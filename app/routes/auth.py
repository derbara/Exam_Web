from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import bcrypt

from app.models import User, db
from app.utils import get_current_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"]) # Маршрут для страницы входа, обрабатывающий как GET-запросы для отображения формы, так и POST-запросы для аутентификации пользователя
def login(): # Функция для обработки логики входа пользователя, проверяющая введенные данные и устанавливающая сессию при успешной аутентификации, с перенаправлением на главную страницу или страницу, указанную в параметре "next"
    if get_current_user():
        return redirect(url_for("books.index"))

    if request.method == "POST":
        login_value = request.form.get("login", "").strip()
        password = request.form.get("password", "")
        remember = request.form.get("remember")

        user = User.query.filter_by(login=login_value).first()

        if user and user.password_hash and bcrypt.checkpw(
            password.encode("utf-8"), user.password_hash.encode("utf-8")
        ):
            session.clear()
            session["user_id"] = user.id
            session["role_name"] = user.role_name
            session.permanent = bool(remember)

            next_page = request.args.get("next") or url_for("books.index")
            return redirect(next_page)

        flash(
            "Невозможно аутентифицироваться с указанными логином и паролем",
            "danger",
        )
        return render_template( # При неудачной аутентификации повторно отображаем страницу входа с сохранением введенного логина и состояния чекбокса "запомнить меня"
            "login.html",
            login_value=login_value,
            remember=remember,
        )

    return render_template("login.html")


@auth_bp.route("/logout") # Маршрут для выхода из системы, который очищает сессию и перенаправляет пользователя на главную страницу или страницу, указанную в параметре "next"
def logout():
    session.clear()
    next_page = request.args.get("next") or url_for("books.index")
    return redirect(next_page)
