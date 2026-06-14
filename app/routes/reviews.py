from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import sanitize_markdown
from app.decorators import login_required
from app.models import Book, Review, db
from app.utils import get_current_user

reviews_bp = Blueprint("reviews", __name__)

RATING_LABELS = { # Словарь для отображения текстовых меток рейтингов от 0 до 5, который будет использоваться в шаблонах для отображения понятных описаний рейтингов, выставленных пользователями в рецензиях
    5: "отлично",
    4: "хорошо",
    3: "удовлетворительно",
    2: "неудовлетворительно",
    1: "плохо",
    0: "ужасно",
}


@reviews_bp.route("/books/<int:book_id>/reviews/add", methods=["GET", "POST"])
@login_required
def add(book_id): # Маршрут для добавления рецензии на книгу, который обрабатывает как GET-запросы для отображения формы, так и POST-запросы для сохранения рецензии в базе данных, с проверкой прав доступа, существования книги, наличия уже оставленной рецензии, валидацией данных формы, санитизацией текста рецензии, и отображением сообщений об успехе или неудаче
    user = get_current_user()
    if user["role_name"] not in ("admin", "moderator", "user"):
        flash(
            "У вас недостаточно прав для выполнения данного действия",
            "danger",
        )
        return redirect(url_for("books.index"))

    book = Book.query.get(book_id) # Извлекаем книгу по ID, чтобы проверить ее существование и отобразить информацию о ней в форме добавления рецензии. Если книга не найдена, перенаправляем на главную страницу с предупреждением
    if not book:
        flash("Книга не найдена.", "warning")
        return redirect(url_for("books.index"))

    existing = Review.query.filter_by(book_id=book_id, user_id=user["id"]).first()

    if existing:
        flash("Вы уже оставляли рецензию на эту книгу.", "info")
        return redirect(url_for("books.view", book_id=book_id))

    form_data = {
        "rating": request.form.get("rating", "5"),
        "text": request.form.get("text", "").strip(),
    }

    if request.method == "POST":
        rating = form_data["rating"]
        if not rating.isdigit() or int(rating) not in RATING_LABELS:
            flash(
                "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
                "danger",
            )
            return render_template(
                "reviews/form.html",
                book=book,
                form_data=form_data,
                rating_labels=RATING_LABELS,
            )

        if not form_data["text"]:
            flash(
                "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
                "danger",
            )
            return render_template(
                "reviews/form.html",
                book=book,
                form_data=form_data,
                rating_labels=RATING_LABELS,
            )

        sanitized_text = sanitize_markdown(form_data["text"])
        try:
            review = Review(book_id=book_id, user_id=user["id"], rating=int(rating), text=sanitized_text)
            db.session.add(review)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash(
                "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
                "danger",
            )
            return render_template(
                "reviews/form.html",
                book=book,
                form_data=form_data,
                rating_labels=RATING_LABELS,
            )

        flash("Рецензия успешно добавлена.", "success")
        return redirect(url_for("books.view", book_id=book_id))

    return render_template( # При GET-запросе отображаем форму добавления рецензии, передавая в шаблон информацию о книге, данные формы (которые будут пустыми при первом отображении) и словарь с метками рейтингов для отображения в форме
        "reviews/form.html",
        book=book,
        form_data=form_data,
        rating_labels=RATING_LABELS,
    )
