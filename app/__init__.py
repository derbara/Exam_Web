import os
import sqlite3
from datetime import timedelta

import bcrypt
import bleach
import markdown
from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.config import Config
from app.models import db


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.permanent_session_lifetime = timedelta(days=30)

    db.init_app(app)

    upload_dir = app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)

    from app.routes.auth import auth_bp
    from app.routes.books import books_bp
    from app.routes.collections import collections_bp
    from app.routes.reviews import reviews_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(collections_bp)

    with app.app_context():
        db.create_all()
        seed_initial_data()

    @app.context_processor
    def inject_user():
        from flask import session

        from app.utils import get_current_user

        return {"current_user": get_current_user()}

    return app


def seed_initial_data():
    from app.models import Book, Collection, Cover, Genre, Review, Role, User

    if Role.query.count() == 0:
        roles = [
            Role(name="admin", description="Суперпользователь с полным доступом к системе"),
            Role(name="moderator", description="Может редактировать данные книг и модерировать рецензии"),
            Role(name="user", description="Может оставлять рецензии и управлять подборками"),
        ]
        db.session.add_all(roles)

    if Genre.query.count() == 0:
        genres = [
            Genre(name="Роман"),
            Genre(name="Фантастика"),
            Genre(name="Детектив"),
            Genre(name="Научная литература"),
            Genre(name="Поэзия"),
            Genre(name="История"),
            Genre(name="Биография"),
            Genre(name="Приключения"),
        ]
        db.session.add_all(genres)

    if User.query.count() == 0:
        admin_role = Role.query.filter_by(name="admin").first()
        moderator_role = Role.query.filter_by(name="moderator").first()
        user_role = Role.query.filter_by(name="user").first()
        password_hash = bcrypt.hashpw(b"password", bcrypt.gensalt()).decode("utf-8")
        demo_users = [
            User(login="admin", password_hash=password_hash, last_name="Комар", first_name="Ярослава", middle_name="Руслановна", role_id=admin_role.id),
            User(login="moderator", password_hash=password_hash, last_name="Иванов", first_name="Иван", middle_name="Иванович", role_id=moderator_role.id),
            User(login="reader", password_hash=password_hash, last_name="Петров", first_name="Пётр", middle_name=None, role_id=user_role.id),
        ]
        db.session.add_all(demo_users)

    db.session.commit()


def sanitize_markdown(text):
    if not text:
        return ""
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union(
        {
            "p",
            "br",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "pre",
            "code",
            "blockquote",
            "ul",
            "ol",
            "li",
            "strong",
            "em",
            "a",
            "hr",
        }
    )
    allowed_attributes = {
        **bleach.sanitizer.ALLOWED_ATTRIBUTES,
        "a": ["href", "title", "rel"],
    }
    return bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True,
    )


def render_markdown(text):
    sanitized = sanitize_markdown(text)
    html = markdown.markdown(
        sanitized,
        extensions=["extra", "nl2br", "sane_lists"],
    )
    return bleach.linkify(html)
