import os

from flask import session

from app.models import User


def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None

    user = User.query.get(user_id)
    if not user:
        return None

    return {
        "id": user.id,
        "login": user.login,
        "last_name": user.last_name,
        "first_name": user.first_name,
        "middle_name": user.middle_name,
        "role_name": user.role_name,
        "role_description": user.role.description if user.role else None,
    }


def user_full_name(user):
    if not user:
        return ""
    parts = [user["last_name"], user["first_name"]]
    if user.get("middle_name"):
        parts.append(user["middle_name"])
    return " ".join(parts)


def allowed_file(filename, allowed_extensions):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


def delete_cover_file(upload_folder, filename):
    if not filename:
        return
    path = os.path.join(upload_folder, filename)
    if os.path.isfile(path):
        os.remove(path)
