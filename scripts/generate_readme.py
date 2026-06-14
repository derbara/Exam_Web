#!/usr/bin/env python3
"""Generate Russian README with UTF-8 encoding."""

from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.ru.md"

CONTENT = """# \u0410\u0418\u0421 \u00ab\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430\u00bb

** \u0413\u0440. 241-3211 \u041a\u043e\u043c\u0430\u0440 \u042f\u0440\u043e\u0441\u043b\u0430\u0432\u0430 \u0420\u0443\u0441\u043b\u0430\u043d\u043e\u0432\u043d\u0430 **

## \u0421\u0442\u0435\u043a

Python 3.11+, Flask 3, MySQL 8, Bootstrap 5, EasyMDE, Bleach, Markdown.

## \u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u043d\u0430 MacBook M4

### 1. \u0421\u0438\u0441\u0442\u0435\u043c\u043d\u044b\u0435 \u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438

```bash
xcode-select --install
brew install mysql pkg-config
brew services start mysql
mysql_secure_installation
```

### 2. \u0412\u0438\u0440\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0435 \u043e\u043a\u0440\u0443\u0436\u0435\u043d\u0438\u0435

```bash
cd ~/Documents/electronic-library
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
export PKG_CONFIG_PATH="$(brew --prefix mysql)/lib/pkgconfig"
pip install -r requirements.txt
```

\u0415\u0441\u043b\u0438 \u043e\u0448\u0438\u0431\u043a\u0430 \u0441\u0431\u043e\u0440\u043a\u0438 `mysqlclient`:

```bash
brew install mysql-client
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
export LDFLAGS="-L$(brew --prefix mysql-client)/lib"
export CPPFLAGS="-I$(brew --prefix mysql-client)/include"
pip install mysqlclient
pip install -r requirements.txt
```

### 3. \u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 `.env`

```bash
cp .env.example .env
python3 -c "import secrets; print(secrets.token_hex(32))"
```

\u0412\u0441\u0442\u0430\u0432\u044c\u0442\u0435 \u0441\u0433\u0435\u043d\u0435\u0440\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u043a\u043b\u044e\u0447 \u0432 `SECRET_KEY`.

### 4. \u0418\u043d\u0438\u0446\u0438\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f \u0411\u0414

** \u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438: **

```bash
chmod +x scripts/init_db.sh
./scripts/init_db.sh
```

** \u0412\u0440\u0443\u0447\u043d\u0443\u044e: **

```bash
mysql -u root -p < migrations/init.sql
mysql -u root -p -e "CREATE USER IF NOT EXISTS 'library_user'@'localhost' IDENTIFIED BY 'library_pass'; GRANT ALL PRIVILEGES ON electronic_library.* TO 'library_user'@'localhost'; FLUSH PRIVILEGES;"
python3 scripts/seed_db.py
python3 scripts/generate_templates.py
```

### 5. \u0417\u0430\u043f\u0443\u0441\u043a

```bash
source venv/bin/activate
python run.py
```

\u0411\u0440\u0430\u0443\u0437\u0435\u0440: http://127.0.0.1:5000

## \u0422\u0435\u0441\u0442\u043e\u0432\u044b\u0435 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438

| \u041b\u043e\u0433\u0438\u043d | \u041f\u0430\u0440\u043e\u043b\u044c | \u0420\u043e\u043b\u044c |
|-------|----------|------|
| admin | password123 | \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440 |
| moderator | password123 | \u043c\u043e\u0434\u0435\u0440\u0430\u0442\u043e\u0440 |
| reader | password123 | \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c |

## \u0421\u0445\u0435\u043c\u0430 \u0411\u0414

- `roles` \u2014 \u0440\u043e\u043b\u0438 (admin, moderator, user)
- `users` \u2014 \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0438
- `genres`, `books`, `book_genres`
- `covers` \u2014 \u043e\u0431\u043b\u043e\u0436\u043a\u0438 (\u0441 MD5-\u0434\u0435\u0434\u0443\u043f\u043b\u0438\u043a\u0430\u0446\u0438\u0435\u0439 \u0444\u0430\u0439\u043b\u043e\u0432)
- `reviews` \u2014 \u0440\u0435\u0446\u0435\u043d\u0437\u0438\u0438
- `collections`, `collection_books` \u2014 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0438

\u041c\u0438\u0433\u0440\u0430\u0446\u0438\u044f: `migrations/init.sql`

## \u041f\u043e\u043b\u0435\u0437\u043d\u044b\u0435 \u043a\u043e\u043c\u0430\u043d\u0434\u044b

```bash
source venv/bin/activate
python3 scripts/seed_db.py
python3 scripts/generate_templates.py
mysql -u library_user -p electronic_library
brew services stop mysql
```

## \u0420\u0435\u0430\u043b\u0438\u0437\u043e\u0432\u0430\u043d\u043d\u044b\u0439 \u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b

- \u041a\u0430\u0442\u0430\u043b\u043e\u0433 \u043a\u043d\u0438\u0433 \u0441 \u043f\u0430\u0433\u0438\u043d\u0430\u0446\u0438\u0435\u0439 (10 \u043d\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0443)
- CRUD \u043a\u043d\u0438\u0433 \u0441 \u043e\u0431\u043b\u043e\u0436\u043a\u0430\u043c\u0438 \u0438 Markdown (EasyMDE + Bleach)
- \u0420\u0435\u0446\u0435\u043d\u0437\u0438\u0438 \u0441 \u043e\u0446\u0435\u043d\u043a\u0430\u043c\u0438 0\u20135
- \u041f\u043e\u0434\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0440\u043e\u043b\u0438 \u00ab\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u00bb
- \u041c\u043e\u0434\u0430\u043b\u044c\u043d\u044b\u0435 \u043e\u043a\u043d\u0430 Bootstrap
- \u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u0440\u0430\u0432 \u0438 flash-\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f
"""

if __name__ == "__main__":
    README.write_text(CONTENT, encoding="utf-8")
    print(f"Wrote {README}")
