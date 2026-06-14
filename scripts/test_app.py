#!/usr/bin/env python3
"""Integration tests for the electronic library application."""

import io
import os
import sys

# Minimal valid 1x1 PNG
PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx"
    b"\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app import create_app
from app.models import Book, Collection, Genre, Review, User, db


def login_as(client, login):
    with client.session_transaction() as sess:
        user = User.query.filter_by(login=login).first()
        sess.clear()
        sess["user_id"] = user.id


def run_tests():
    app = create_app()
    errors = []

    with app.app_context():
        client = app.test_client()

        def check(name, condition, detail=""):
            if not condition:
                errors.append(f"{name}: {detail}")
            else:
                print(f"OK: {name}")

        r = client.get("/")
        check("Index page", r.status_code == 200)

        r = client.get("/login")
        check("Login page", r.status_code == 200)

        r = client.post(
            "/login",
            data={"login": "wrong", "password": "wrong"},
            follow_redirects=True,
        )
        check(
            "Invalid login message",
            "Невозможно аутентифицироваться" in r.data.decode(),
        )

        r = client.post(
            "/login",
            data={"login": "admin", "password": "password"},
            follow_redirects=True,
        )
        check("Admin login", r.status_code == 200)

        with client.session_transaction() as sess:
            sess.clear()

        r = client.get("/books/add", follow_redirects=True)
        check(
            "Unauthenticated add redirect",
            "необходимо пройти процедуру аутентификации" in r.data.decode(),
        )

        login_as(client, "reader")
        r = client.get("/books/add", follow_redirects=True)
        check(
            "Reader denied add book",
            "недостаточно прав" in r.data.decode(),
        )

        login_as(client, "admin")
        genre = Genre.query.first()
        from werkzeug.datastructures import FileStorage

        data = {
            "title": "Test Book",
            "short_description": "Test **description**",
            "year": "2024",
            "publisher": "Test Pub",
            "author": "Test Author",
            "pages_volume": "300",
            "genre_ids": [str(genre.id)],
            "cover": FileStorage(
                stream=io.BytesIO(PNG_BYTES),
                filename="cover.png",
                content_type="image/png",
            ),
        }
        r = client.post("/books/add", data=data, follow_redirects=False)
        check("Add book", r.status_code == 302, f"status={r.status_code}")

        book = Book.query.filter_by(title="Test Book").first()
        check("Book created", book is not None)
        if not book:
            return errors

        book_id = book.id
        r = client.get(f"/books/{book_id}")
        check("Book view", r.status_code == 200)
        html = r.data.decode()
        check("Book description rendered", "description" in html.lower())
        check("Genres displayed", genre.name in html)

        login_as(client, "reader")
        r = client.post(
            "/collections/add",
            data={"name": "My Collection"},
            follow_redirects=True,
        )
        check("Add collection", "успешно добавлена" in r.data.decode())

        collection = Collection.query.filter_by(name="My Collection").first()
        check("Collection created", collection is not None)

        r = client.get("/collections")
        check("Collections list", r.status_code == 200)

        r = client.post(
            f"/books/{book_id}/add-to-collection",
            data={"collection_id": str(collection.id)},
            follow_redirects=True,
        )
        check(
            "Add book to collection",
            "успешно добавлена" in r.data.decode(),
        )

        r = client.get(f"/collections/{collection.id}")
        check("Collection view", r.status_code == 200)
        check(
            "Collection has book",
            "Test Book" in r.data.decode(),
        )

        r = client.post(
            f"/books/{book_id}/reviews/add",
            data={"rating": "5", "text": "Great **book**!"},
            follow_redirects=True,
        )
        check("Add review", "успешно добавлена" in r.data.decode())

        r = client.get(f"/books/{book_id}/reviews/add", follow_redirects=True)
        check(
            "Duplicate review blocked",
            "уже оставляли" in r.data.decode(),
        )

        login_as(client, "admin")
        r = client.post(f"/books/{book_id}/delete", follow_redirects=True)
        check("Delete book", "успешно удалена" in r.data.decode())
        check("Book removed from DB", Book.query.get(book_id) is None)

    return errors


if __name__ == "__main__":
    errors = run_tests()
    if errors:
        print("\nFAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print("\nAll tests passed.")
