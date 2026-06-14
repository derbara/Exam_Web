import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def _build_database_uri(): # Функция для построения URI подключения к базе данных, поддерживающая MySQL и SQLite
    mysql_host = os.getenv("MYSQL_HOST")
    if mysql_host:
        user = os.getenv("MYSQL_USER", "library_user")
        password = os.getenv("MYSQL_PASSWORD", "library_pass")
        port = os.getenv("MYSQL_PORT", "3306")
        database = os.getenv("MYSQL_DB", "electronic_library")
        return (
            f"mysql+pymysql://{user}:{password}@{mysql_host}:{port}/{database}"
            "?charset=utf8mb4"
        )
    return f"sqlite:///{BASE_DIR / 'app.db'}"


class Config: # Класс конфигурации для приложения Flask, загружающий настройки из переменных окружения и задающий значения по умолчанию
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.getenv( 
        "UPLOAD_FOLDER",
        str(BASE_DIR / "app" / "static" / "uploads" / "covers"),
    )
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)) # Максимальный размер загружаемых файлов (16 МБ по умолчанию)
    ALLOWED_COVER_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    BOOKS_PER_PAGE = 10 # Количество книг, отображаемых на одной странице при пагинации

    ROLE_ADMIN = "admin"
    ROLE_MODERATOR = "moderator"
    ROLE_USER = "user"
