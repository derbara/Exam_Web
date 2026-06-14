import os

from flask import session

from app.models import User


def get_current_user(): # Функция для получения информации о текущем аутентифицированном пользователе из базы данных, возвращающая словарь с данными пользователя или None, если пользователь не найден или не аутентифицирован
    user_id = session.get("user_id")
    if not user_id:
        return None

    user = User.query.get(user_id)
    if not user:
        return None

    return { # Возвращаем словарь с данными пользователя, включая его ID, логин, имя и роль, а также описание роли, если роль установлена
        "id": user.id,
        "login": user.login,
        "last_name": user.last_name,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "role_name": user.role_name,
        "role_description": user.role.description if user.role else None,
    }


def user_full_name(user): # Функция для получения полного имени пользователя в виде строки, объединяющей фамилию, имя и отчество (если есть), возвращающая пустую строку, если пользователь не найден
    if not user:
        return ""
    parts = [user["last_name"], user["first_name"]]
    if user.get("middle_name"):
        parts.append(user["middle_name"])
    return " ".join(parts)


def allowed_file(filename, allowed_extensions): # Функция для проверки, имеет ли имя файла разрешенное расширение, возвращающая True, если расширение разрешено, и False в противном случае
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


def delete_cover_file(upload_folder, filename): # Функция для удаления файла обложки книги из папки загрузок, если имя файла указано и файл существует, с безопасной обработкой отсутствия файла
    if not filename:
        return
    path = os.path.join(upload_folder, filename) # Получаем полный путь к файлу обложки, используя папку загрузок и имя файла
    if os.path.isfile(path):
        os.remove(path)
