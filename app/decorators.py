from functools import wraps

from flask import flash, redirect, session, url_for

from app.config import Config
from app.utils import get_current_user


def login_required(view): # Декоратор для защиты маршрутов, требующих аутентификации, перенаправляющий неавторизованных пользователей на страницу входа
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            flash(
                "Для выполнения данного действия необходимо пройти процедуру аутентификации",
                "warning",
            )
            return redirect(url_for("auth.login", next=request_path()))
        return view(*args, **kwargs)

    return wrapped


def role_required(*roles): # Декоратор для защиты маршрутов, требующих определенных ролей, перенаправляющий пользователей без нужных прав на главную страницу
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = get_current_user()
            if not user:
                flash(
                    "Для выполнения данного действия необходимо пройти процедуру аутентификации",
                    "warning",
                )
                return redirect(url_for("auth.login", next=request_path()))
            if user["role_name"] not in roles:
                flash(
                    "У вас недостаточно прав для выполнения данного действия",
                    "danger",
                )
                return redirect(url_for("books.index"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def admin_required(view): # Декоратор для защиты маршрутов, доступных только администраторам
    return role_required(Config.ROLE_ADMIN)(view)


def editor_required(view): # Декоратор для защиты маршрутов, доступных администраторам и модераторам
    return role_required(Config.ROLE_ADMIN, Config.ROLE_MODERATOR)(view)


def regular_user_required(view): # Декоратор для защиты маршрутов, доступных всем аутентифицированным пользователям, независимо от роли
    return role_required(Config.ROLE_USER)(view)


def request_path(): # Функция для получения полного пути текущего запроса, включая строку запроса, для корректного перенаправления после аутентификации
    from flask import request

    return request.full_path if request.query_string else request.path
