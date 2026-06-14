from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.decorators import regular_user_required
from app.models import Book, Collection, db
from app.utils import get_current_user

collections_bp = Blueprint("collections", __name__)


@collections_bp.route("/collections") # Маршрут для страницы со списком подборок текущего пользователя, доступный всем аутентифицированным пользователям, который извлекает подборки из базы данных, считает количество книг в каждой подборке, и отображает страницу со списком подборок
@regular_user_required
def index():
    user = get_current_user()
    collections = (
        Collection.query.filter_by(user_id=user["id"])
        .order_by(Collection.name)
        .all()
    )
    for collection in collections:
        collection.book_count = len(collection.books)

    return render_template("collections/list.html", collections=collections)


@collections_bp.route("/collections/add", methods=["POST"]) # Маршрут для добавления новой подборки, доступный всем аутентифицированным пользователям, который обрабатывает POST-запросы с данными новой подборки, сохраняет ее в базе данных, и перенаправляет обратно на страницу со списком подборок с сообщением об успехе или неудаче
@regular_user_required
def add():
    user = get_current_user()
    name = request.form.get("name", "").strip()

    if not name:
        flash(
            "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
            "danger",
        )
        return redirect(url_for("collections.index"))

    try:
        collection = Collection(name=name, user_id=user["id"])
        db.session.add(collection)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash(
            "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
            "danger",
        )
        return redirect(url_for("collections.index"))

    flash(f'Подборка «{name}» успешно добавлена.', "success")
    return redirect(url_for("collections.index"))


@collections_bp.route("/collections/<int:collection_id>")
@regular_user_required
def view(collection_id): # Маршрут для страницы просмотра подборки, который извлекает подборку по ID, проверяет ее существование, получает связанные книги, и отображает страницу с подробной информацией о подборке
    user = get_current_user()
    collection = Collection.query.filter_by(id=collection_id, user_id=user["id"]).first()
    if not collection:
        flash("Подборка не найдена.", "warning")
        return redirect(url_for("collections.index"))

    books = [
        {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
        }
        for book in collection.books
    ]

    return render_template(
        "collections/view.html",
        collection=collection,
        books=books,
    )


@collections_bp.route("/books/<int:book_id>/add-to-collection", methods=["POST"])
@regular_user_required
def add_book_to_collection(book_id): # Маршрут для добавления книги в подборку, который обрабатывает POST-запросы с ID книги и ID подборки, проверяет их существование и принадлежность к текущему пользователю, сохраняет связь между книгой и подборкой в базе данных, и перенаправляет обратно на страницу книги с сообщением об успехе или неудаче
    user = get_current_user()
    collection_id = request.form.get("collection_id")

    if not collection_id or not collection_id.isdigit():
        flash(
            "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
            "danger",
        )
        return redirect(url_for("books.view", book_id=book_id))

    if not Book.query.get(book_id):
        flash("Книга не найдена.", "warning")
        return redirect(url_for("books.index"))

    collection = Collection.query.filter_by(id=int(collection_id), user_id=user["id"]).first()

    if not collection:
        flash("Подборка не найдена.", "warning")
        return redirect(url_for("books.view", book_id=book_id))

    try:
        if not any(book.id == book_id for book in collection.books):
            collection.books.append(Book.query.get(book_id))
            db.session.commit()
    except Exception:
        db.session.rollback()
        flash(
            "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
            "danger",
        )
        return redirect(url_for("books.view", book_id=book_id))

    flash(f'Книга успешно добавлена в подборку «{collection.name}».', "success")
    return redirect(url_for("books.view", book_id=book_id))
