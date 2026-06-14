import hashlib
import os

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.utils import secure_filename

from app import render_markdown, sanitize_markdown
from app.decorators import admin_required, editor_required
from app.models import Book, Collection, Cover, Genre, Review, User, db
from app.utils import allowed_file, delete_cover_file, get_current_user

books_bp = Blueprint("books", __name__)


def _get_genres():
    return Genre.query.order_by(Genre.name).all()


def _parse_book_form():
    return {
        "title": request.form.get("title", "").strip(),
        "short_description": request.form.get("short_description", "").strip(),
        "year": request.form.get("year", "").strip(),
        "publisher": request.form.get("publisher", "").strip(),
        "author": request.form.get("author", "").strip(),
        "pages_volume": request.form.get("pages_volume", "").strip(),
        "genre_ids": request.form.getlist("genre_ids"),
    }


def _validate_book_form(data, require_cover=False):
    errors = []
    if not data["title"]:
        errors.append("title")
    if not data["short_description"]:
        errors.append("short_description")
    if not data["year"].isdigit() or not (1000 <= int(data["year"]) <= 9999):
        errors.append("year")
    if not data["publisher"]:
        errors.append("publisher")
    if not data["author"]:
        errors.append("author")
    if not data["pages_volume"].isdigit() or int(data["pages_volume"]) <= 0:
        errors.append("pages_volume")
    if not data["genre_ids"]:
        errors.append("genre_ids")
    if require_cover:
        cover = request.files.get("cover")
        if not cover or not cover.filename:
            errors.append("cover")
        elif not allowed_file(
            cover.filename,
            current_app.config["ALLOWED_COVER_EXTENSIONS"],
        ):
            errors.append("cover")
    return errors


def _save_book_genres(book, genre_ids):
    book.genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()


def _save_cover(book, cover_file):
    file_data = cover_file.read()
    md5_hash = hashlib.md5(file_data).hexdigest()
    mime_type = cover_file.mimetype or "application/octet-stream"

    existing = Cover.query.filter_by(md5_hash=md5_hash).first()
    if existing:
        cover = Cover(filename=existing.filename, mime_type=existing.mime_type, md5_hash=md5_hash, book=book)
        db.session.add(cover)
        db.session.flush()
        return cover.id, existing.filename, None

    cover = Cover(filename="pending", mime_type=mime_type, md5_hash=md5_hash, book=book)
    db.session.add(cover)
    db.session.flush()
    ext = secure_filename(cover_file.filename).rsplit(".", 1)[-1].lower()
    filename = f"{cover.id}.{ext}"
    cover.filename = filename
    return cover.id, filename, file_data


@books_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["BOOKS_PER_PAGE"]
    offset = (page - 1) * per_page

    total = Book.query.count()
    books = (
        Book.query.order_by(Book.year.desc(), Book.id.desc())
        .offset(offset)
        .limit(per_page)
        .all()
    )

    for book in books:
        book.genres = sorted(book.genres, key=lambda g: g.name)

    total_pages = max(1, (total + per_page - 1) // per_page)
    user = get_current_user()

    return render_template(
        "index.html",
        books=books,
        page=page,
        total_pages=total_pages,
        user=user,
    )


@books_bp.route("/books/add", methods=["GET", "POST"])
@admin_required
def add():
    genres = _get_genres()
    form_data = _parse_book_form()

    if request.method == "POST":
        errors = _validate_book_form(form_data, require_cover=True)
        if errors:
            flash(
                "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
                "danger",
            )
            return render_template(
                "books/add.html",
                genres=genres,
                form_data=form_data,
                is_edit=False,
            )

        cover_file = request.files["cover"]
        sanitized_description = sanitize_markdown(form_data["short_description"])
        file_data = None
        filename = None

        try:
            book = Book(
                title=form_data["title"],
                short_description=sanitized_description,
                year=int(form_data["year"]),
                publisher=form_data["publisher"],
                author=form_data["author"],
                pages_volume=int(form_data["pages_volume"]),
            )
            db.session.add(book)
            db.session.flush()
            _save_book_genres(book, form_data["genre_ids"])
            _, filename, file_data = _save_cover(book, cover_file)
            db.session.commit()
            book_id = book.id
        except Exception:
            db.session.rollback()
            flash(
                "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
                "danger",
            )
            return render_template(
                "books/add.html",
                genres=genres,
                form_data=form_data,
                is_edit=False,
            )
        if file_data and filename:
            upload_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], filename
            )
            with open(upload_path, "wb") as f:
                f.write(file_data)

        flash("Книга успешно добавлена.", "success")
        return redirect(url_for("books.view", book_id=book_id))

    return render_template(
        "books/add.html",
        genres=genres,
        form_data=form_data,
        is_edit=False,
    )


@books_bp.route("/books/<int:book_id>/edit", methods=["GET", "POST"])
@editor_required
def edit(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash("Книга не найдена.", "warning")
        return redirect(url_for("books.index"))

    selected_genres = [genre.id for genre in book.genres]

    genres = _get_genres()
    form_data = _parse_book_form() if request.method == "POST" else {
        "title": book.title,
        "short_description": book.short_description,
        "year": str(book.year),
        "publisher": book.publisher,
        "author": book.author,
        "pages_volume": str(book.pages_volume),
        "genre_ids": [str(g) for g in selected_genres],
    }

    if request.method == "POST":
        errors = _validate_book_form(form_data, require_cover=False)
        if errors:
            flash(
                "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
                "danger",
            )
            return render_template(
                "books/edit.html",
                genres=genres,
                form_data=form_data,
                book=book,
                is_edit=True,
            )

        sanitized_description = sanitize_markdown(form_data["short_description"])
        try:
            book.title = form_data["title"]
            book.short_description = sanitized_description
            book.year = int(form_data["year"])
            book.publisher = form_data["publisher"]
            book.author = form_data["author"]
            book.pages_volume = int(form_data["pages_volume"])
            _save_book_genres(book, form_data["genre_ids"])
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash(
                "При сохранении данных возникла ошибка. Проверьте корректность введённых данных.",
                "danger",
            )
            return render_template(
                "books/edit.html",
                genres=genres,
                form_data=form_data,
                book=book,
                is_edit=True,
            )

        flash("Данные книги успешно обновлены.", "success")
        return redirect(url_for("books.view", book_id=book_id))

    return render_template(
        "books/edit.html",
        genres=genres,
        form_data=form_data,
        book=book,
        is_edit=True,
    )


@books_bp.route("/books/<int:book_id>/delete", methods=["POST"])
@admin_required
def delete(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash("Книга не найдена.", "warning")
        return redirect(url_for("books.index"))

    cover = book.cover
    filename_to_check = cover.filename if cover else None

    try:
        db.session.delete(book)
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash("Не удалось удалить книгу.", "danger")
        return redirect(url_for("books.index"))

    if filename_to_check:
        remaining = Cover.query.filter_by(filename=filename_to_check).count()
        if remaining == 0:
            delete_cover_file(current_app.config["UPLOAD_FOLDER"], filename_to_check)

    flash(f'Книга «{book.title}» успешно удалена.', "success")
    return redirect(url_for("books.index"))


@books_bp.route("/books/<int:book_id>")
def view(book_id):
    book = Book.query.get(book_id)
    if not book:
        flash("Книга не найдена.", "warning")
        return redirect(url_for("books.index"))

    book.genres = sorted(book.genres, key=lambda g: g.name)
    book.description_html = render_markdown(book.short_description)

    cover = book.cover

    reviews = []
    for review in Review.query.filter_by(book_id=book_id).order_by(Review.created_at.desc()).all():
        data = {
            "id": review.id,
            "rating": review.rating,
            "text": review.text,
            "created_at": review.created_at,
            "text_html": render_markdown(review.text),
            "author_name": review.author_name,
        }
        reviews.append(data)

    user = get_current_user()
    user_review = None
    user_collections = []

    if user:
        user_review_obj = Review.query.filter_by(book_id=book_id, user_id=user["id"]).first()
        if user_review_obj:
            user_review = {
                "id": user_review_obj.id,
                "rating": user_review_obj.rating,
                "text": user_review_obj.text,
                "created_at": user_review_obj.created_at,
                "text_html": render_markdown(user_review_obj.text),
            }

        if user["role_name"] == "user":
            user_collections = [
                {"id": c.id, "name": c.name}
                for c in Collection.query.filter_by(user_id=user["id"]).order_by(Collection.name).all()
            ]

    return render_template(
        "books/view.html",
        book=book,
        cover=cover,
        reviews=reviews,
        user=user,
        user_review=user_review,
        user_collections=user_collections,
    )
