#!/usr/bin/env python3
"""Seed roles, genres and demo users with bcrypt password hashes."""

import os
import sys

import bcrypt
import pymysql
from dotenv import load_dotenv

load_dotenv()

PASSWORD = "password"


def main():
    conn = pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "library_user"),
        password=os.getenv("MYSQL_PASSWORD", "library_pass"),
        database=os.getenv("MYSQL_DB", "electronic_library"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    password_hash = bcrypt.hashpw(
        PASSWORD.encode("utf-8"), bcrypt.gensalt(rounds=12)
    ).decode("utf-8")

    roles = [
        ("admin", "Суперпользователь с полным доступом к системе"),
        ("moderator", "Может редактировать данные книг и модерировать рецензии"),
        ("user", "Может оставлять рецензии и управлять подборками"),
    ]
    genres = [
        "Роман",
        "Фантастика",
        "Детектив",
        "Научная литература",
        "Поэзия",
        "История",
        "Биография",
        "Приключения",
    ]
    users = [
        ("admin", "Комар", "Ярослава", "Руслановна", "admin"),
        ("moderator", "Иванов", "Иван", "Иванович", "moderator"),
        ("reader", "Петров", "Пётр", None, "user"),
    ]

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS cnt FROM roles")
        if cur.fetchone()["cnt"] > 0:
            print("Database already seeded. Skipping.")
            conn.close()
            return

        for name, description in roles:
            cur.execute(
                "INSERT INTO roles (name, description) VALUES (%s, %s)",
                (name, description),
            )

        for genre in genres:
            cur.execute("INSERT INTO genres (name) VALUES (%s)", (genre,))

        for login, last_name, first_name, middle_name, role_name in users:
            cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
            role_id = cur.fetchone()["id"]
            cur.execute(
                """
                INSERT INTO users
                    (login, password_hash, last_name, first_name, middle_name, role_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    login,
                    password_hash,
                    last_name,
                    first_name,
                    middle_name,
                    role_id,
                ),
            )

    conn.commit()
    conn.close()
    print("Seed completed.")
    print(f"Demo password for admin/moderator/reader: {PASSWORD}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Seed failed: {exc}", file=sys.stderr)
        sys.exit(1)
