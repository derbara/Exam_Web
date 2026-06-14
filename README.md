## 1. Что используется

Проект реализован как Flask-приложение и работает с MySQL.

- СУБД: MySQL
- Схема БД и базовые таблицы описаны в [migrations/init.sql](migrations/init.sql)
- Для инициализации данных используется скрипт [scripts/seed_db.py](scripts/seed_db.py)

> В проекте нет отдельного механизма миграций вроде Alembic или Flask-Migrate. Инициализация схемы выполняется вручную через SQL-файл, поэтому под «миграцией» здесь понимается применение схемы из [migrations/init.sql](migrations/init.sql).
## 2. Демо-аккаунты

| Логин | Пароль | Роль |
|-------|--------|------|
| admin | password123 | admin |
| moderator | password123 | moderator |
| reader | password123 | user |
