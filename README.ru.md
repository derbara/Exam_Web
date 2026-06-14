# Подробная инструкция по запуску проекта

## 1. Что используется

Проект реализован как Flask-приложение и работает с MySQL.

- СУБД: MySQL
- Схема БД и базовые таблицы описаны в [migrations/init.sql](migrations/init.sql)
- Для инициализации данных используется скрипт [scripts/seed_db.py](scripts/seed_db.py)

> В проекте нет отдельного механизма миграций вроде Alembic или Flask-Migrate. Инициализация схемы выполняется вручную через SQL-файл, поэтому под «миграцией» здесь понимается применение схемы из [migrations/init.sql](migrations/init.sql).

## 2. Требования

Перед запуском убедитесь, что у вас установлены:

- Python 3.8+
- MySQL
- Homebrew (на macOS)

## 3. Клонирование и подготовка виртуального окружения

```bash
cd electronic-library
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

## 4. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 5. Установка и запуск MySQL

На macOS через Homebrew:

```bash
brew install mysql pkg-config
export PKG_CONFIG_PATH="$(brew --prefix mysql)/lib/pkgconfig"
brew services start mysql
```

Проверьте, что сервер MySQL запущен:

```bash
mysql -u root -p
```

## 6. Настройка переменных окружения

Скопируйте пример файла окружения:

```bash
cp .env.example .env
```

Откройте файл [.env](.env) и проверьте параметры подключения к MySQL. В проекте используются переменные вида:

- MYSQL_HOST
- MYSQL_PORT
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_DB
- SECRET_KEY

Если хотите использовать значения по умолчанию из примера, убедитесь, что в MySQL есть пользователь с логином и паролем, указанными в [.env.example](.env.example), либо измените значения в [.env](.env) под вашу локальную конфигурацию.

### При необходимости создайте пользователя MySQL

```sql
CREATE DATABASE IF NOT EXISTS electronic_library
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'library_user'@'localhost' IDENTIFIED BY 'library_pass';
GRANT ALL PRIVILEGES ON electronic_library.* TO 'library_user'@'localhost';
FLUSH PRIVILEGES;
```

## 7. Инициализация базы данных

Схема базы данных создаётся из файла [migrations/init.sql](migrations/init.sql).

```bash
chmod +x scripts/init_db.sh
./scripts/init_db.sh
```

Скрипт [scripts/init_db.sh](scripts/init_db.sh) делает следующее:

1. копирует [.env.example](.env.example) в [.env](.env), если файл отсутствует;
2. запускает импорт SQL-файла в MySQL.

Если хотите выполнить инициализацию вручную, используйте:

```bash
mysql -u root -p < migrations/init.sql
```

## 8. Заполнение тестовыми данными

После создания таблиц выполните:

```bash
python3 scripts/seed_db.py
```

Этот скрипт добавит:

- роли: admin, moderator, user;
- жанры;
- демо-пользователей;
- демонстрационный пароль: password123.

## 9. Запуск приложения

```bash
python3 run.py
```

Откройте в браузере:

```text
http://127.0.0.1:5000
```

## 10. Демо-аккаунты

| Логин | Пароль | Роль |
|-------|--------|------|
| admin | password123 | admin |
| moderator | password123 | moderator |
| reader | password123 | user |

## 11. Если нужно пересоздать БД с нуля

```bash
mysql -u root -p -e "DROP DATABASE IF EXISTS electronic_library;"
./scripts/init_db.sh
python3 scripts/seed_db.py
```

## 12. Зачем нужен файл [scripts/write_templates.ps1](scripts/write_templates.ps1)

Файл [scripts/write_templates.ps1](scripts/write_templates.ps1) — это вспомогательный PowerShell-скрипт для Windows.

Он нужен для того, чтобы:

- заново сгенерировать HTML-шаблоны проекта;
- сохранить их в UTF-8, чтобы кириллица и спецсимволы корректно отображались;
- упростить обновление шаблонов в среде Windows, где кодировка файлов может быть проблемой.

Он не требуется для обычного запуска приложения, если шаблоны уже существуют. Его используют, когда нужно заново записать шаблоны или исправить их кодировку.

Пример запуска:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/write_templates.ps1
```
