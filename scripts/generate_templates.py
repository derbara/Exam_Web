#!/usr/bin/env python3
"""Generate Jinja2 templates with UTF-8 encoding."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "app" / "templates"


def write(relative_path: str, content: str) -> None:
    path = TEMPLATES / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def main() -> None:
    write(
        "index.html",
        """{% extends "base.html" %}
{% block title %}\u0413\u043b\u0430\u0432\u043d\u0430\u044f \u2014 \u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430{% endblock %}
{% block content %}
<h1 class="mb-4">\u041a\u0430\u0442\u0430\u043b\u043e\u0433 \u043a\u043d\u0438\u0433</h1>
{% if not books %}
<div class="alert alert-info">\u041a\u043d\u0438\u0433\u0438 \u043f\u043e\u043a\u0430 \u043d\u0435 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u044b.</div>
{% else %}
<div class="row g-4">
{% for book in books %}
<div class="col-md-6 col-lg-4">
<div class="card h-100 shadow-sm"><div class="card-body">
<h5 class="card-title">{{ book.title }}</h5>
<p class="card-text text-muted mb-1"><strong>\u0410\u0432\u0442\u043e\u0440:</strong> {{ book.author }}</p>
<p class="card-text mb-1"><strong>\u0416\u0430\u043d\u0440\u044b:</strong> {% if book.genres %}{{ book.genre_names }}{% else %}\u2014{% endif %}</p>
<p class="card-text mb-1"><strong>\u0413\u043e\u0434:</strong> {{ book.year }}</p>
<p class="card-text mb-2"><strong>\u041e\u0446\u0435\u043d\u043a\u0430:</strong> {% if book.review_count > 0 %}{{ '%.1f' | format(book.avg_rating) }} ({{ book.review_count }} \u0440\u0435\u0446.){% else %}\u043d\u0435\u0442 \u043e\u0446\u0435\u043d\u043e\u043a{% endif %}</p>
<div class="btn-group" role="group">
<a href="{{ url_for('books.view', book_id=book.id) }}" class="btn btn-outline-primary btn-sm"><i class="bi bi-eye"></i> \u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440</a>
{% if user and user.role_name in ['admin', 'moderator'] %}
<a href="{{ url_for('books.edit', book_id=book.id) }}" class="btn btn-outline-secondary btn-sm"><i class="bi bi-pencil"></i></a>
{% endif %}
{% if user and user.role_name == 'admin' %}
<button type="button" class="btn btn-outline-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteModal{{ book.id }}"><i class="bi bi-trash"></i></button>
{% endif %}
</div></div></div></div>
{% if user and user.role_name == 'admin' %}
<div class="modal fade" id="deleteModal{{ book.id }}" tabindex="-1"><div class="modal-dialog"><div class="modal-content">
<div class="modal-header"><h5 class="modal-title">\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u043a\u043d\u0438\u0433\u0438</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
<div class="modal-body">\u0412\u044b \u0443\u0432\u0435\u0440\u0435\u043d\u044b, \u0447\u0442\u043e \u0445\u043e\u0442\u0438\u0442\u0435 \u0443\u0434\u0430\u043b\u0438\u0442\u044c \u043a\u043d\u0438\u0433\u0443 \u00ab{{ book.title }}\u00bb?</div>
<div class="modal-footer">
<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">\u041d\u0435\u0442</button>
<form action="{{ url_for('books.delete', book_id=book.id) }}" method="POST" class="d-inline"><button type="submit" class="btn btn-danger">\u0414\u0430</button></form>
</div></div></div></div>
{% endif %}
{% endfor %}
</div>
{% if total_pages > 1 %}
<nav class="mt-4"><ul class="pagination justify-content-center">
<li class="page-item {% if page <= 1 %}disabled{% endif %}"><a class="page-link" href="{{ url_for('books.index', page=page - 1) }}">\u041d\u0430\u0437\u0430\u0434</a></li>
{% for p in range(1, total_pages + 1) %}<li class="page-item {% if p == page %}active{% endif %}"><a class="page-link" href="{{ url_for('books.index', page=p) }}">{{ p }}</a></li>{% endfor %}
<li class="page-item {% if page >= total_pages %}disabled{% endif %}"><a class="page-link" href="{{ url_for('books.index', page=page + 1) }}">\u0412\u043f\u0435\u0440\u0451\u0434</a></li>
</ul></nav>
{% endif %}
{% endif %}
{% if user and user.role_name == 'admin' %}
<div class="mt-4"><a href="{{ url_for('books.add') }}" class="btn btn-success"><i class="bi bi-plus-lg"></i> \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043a\u043d\u0438\u0433\u0443</a></div>
{% endif %}
{% endblock %}
""",
    )

    write(
        "login.html",
        """{% extends "base.html" %}
{% block title %}\u0412\u0445\u043e\u0434 \u2014 \u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430{% endblock %}
{% block content %}
<div class="row justify-content-center"><div class="col-md-5"><div class="card shadow"><div class="card-body p-4">
<h2 class="card-title text-center mb-4">\u0412\u0445\u043e\u0434 \u0432 \u0441\u0438\u0441\u0442\u0435\u043c\u0443</h2>
<form method="POST" action="{{ url_for('auth.login', next=request.args.get('next')) }}">
<div class="mb-3"><label for="login" class="form-label">\u041b\u043e\u0433\u0438\u043d</label><input type="text" class="form-control" id="login" name="login" value="{{ login_value or '' }}" required autofocus></div>
<div class="mb-3"><label for="password" class="form-label">\u041f\u0430\u0440\u043e\u043b\u044c</label><input type="password" class="form-control" id="password" name="password" required></div>
<div class="mb-3 form-check"><input type="checkbox" class="form-check-input" id="remember" name="remember" {% if remember %}checked{% endif %}><label class="form-check-label" for="remember">\u0417\u0430\u043f\u043e\u043c\u043d\u0438\u0442\u044c \u043c\u0435\u043d\u044f</label></div>
<button type="submit" class="btn btn-primary w-100">\u0412\u043e\u0439\u0442\u0438</button>
</form></div></div></div></div>
{% endblock %}
""",
    )

    write(
        "books/_form.html",
        """{% macro book_form(form_data, genres, is_edit=false) %}
<div class="mb-3"><label for="title" class="form-label">\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 *</label><input type="text" class="form-control" id="title" name="title" value="{{ form_data.title or '' }}" required></div>
<div class="mb-3"><label for="author" class="form-label">\u0410\u0432\u0442\u043e\u0440 *</label><input type="text" class="form-control" id="author" name="author" value="{{ form_data.author or '' }}" required></div>
<div class="row">
<div class="col-md-4 mb-3"><label for="year" class="form-label">\u0413\u043e\u0434 *</label><input type="number" class="form-control" id="year" name="year" value="{{ form_data.year or '' }}" min="1000" max="9999" required></div>
<div class="col-md-4 mb-3"><label for="pages_volume" class="form-label">\u041e\u0431\u044a\u0451\u043c (\u0441\u0442\u0440\u0430\u043d\u0438\u0446) *</label><input type="number" class="form-control" id="pages_volume" name="pages_volume" value="{{ form_data.pages_volume or '' }}" min="1" required></div>
<div class="col-md-4 mb-3"><label for="publisher" class="form-label">\u0418\u0437\u0434\u0430\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e *</label><input type="text" class="form-control" id="publisher" name="publisher" value="{{ form_data.publisher or '' }}" required></div>
</div>
<div class="mb-3"><label for="genre_ids" class="form-label">\u0416\u0430\u043d\u0440\u044b *</label>
<select class="form-select" id="genre_ids" name="genre_ids" multiple required size="5">
{% for genre in genres %}<option value="{{ genre.id }}" {% if form_data.genre_ids and genre.id|string in form_data.genre_ids %}selected{% endif %}>{{ genre.name }}</option>{% endfor %}
</select><div class="form-text">\u0423\u0434\u0435\u0440\u0436\u0438\u0432\u0430\u0439\u0442\u0435 Ctrl (Cmd \u043d\u0430 Mac) \u0434\u043b\u044f \u0432\u044b\u0431\u043e\u0440\u0430 \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u0438\u0445 \u0436\u0430\u043d\u0440\u043e\u0432.</div></div>
<div class="mb-3"><label for="short_description" class="form-label">\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 (Markdown) *</label><textarea class="form-control" id="short_description" name="short_description" rows="8">{{ form_data.short_description or '' }}</textarea></div>
{% if not is_edit %}<div class="mb-3"><label for="cover" class="form-label">\u041e\u0431\u043b\u043e\u0436\u043a\u0430 *</label><input type="file" class="form-control" id="cover" name="cover" accept="image/*" required></div>{% endif %}
<button type="submit" class="btn btn-primary">\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c</button><a href="{{ url_for('books.index') }}" class="btn btn-secondary">\u041e\u0442\u043c\u0435\u043d\u0430</a>
{% endmacro %}
""",
    )

    easymde_js = "<script src=\"https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.js\"></script>"
    easymde_css = "<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/easymde/dist/easymde.min.css\">"

    for name, title, multipart in [
        ("add", "\u0414\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043a\u043d\u0438\u0433\u0438", True),
        ("edit", "\u0420\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435 \u043a\u043d\u0438\u0433\u0438", False),
    ]:
        is_edit = name == "edit"
        form_attrs = ' enctype="multipart/form-data"' if multipart else ""
        write(
            f"books/{name}.html",
            f"""{{% extends "base.html" %}}
{{% from "books/_form.html" import book_form %}}
{{% block title %}}{title} \u2014 \u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430{{% endblock %}}
{{% block extra_css %}}{easymde_css}{{% endblock %}}
{{% block content %}}<h1 class="mb-4">{title}</h1><form method="POST"{form_attrs}>{{{{ book_form(form_data, genres, is_edit={str(is_edit).lower()}) }}}}</form>{{% endblock %}}
{{% block extra_js %}}{easymde_js}<script>
const easyMDE = new EasyMDE({{element: document.getElementById('short_description'), spellChecker: false, status: false}});
document.querySelector('form').addEventListener('submit', () => easyMDE.codemirror.save());
</script>{{% endblock %}}
""",
        )

    write(
        "books/view.html",
        """{% extends "base.html" %}
{% block title %}{{ book.title }} \u2014 \u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430{% endblock %}
{% block content %}
<div class="row"><div class="col-md-4 mb-4">{% if cover %}<img src="{{ url_for('static', filename='uploads/covers/' + cover.filename) }}" class="img-fluid rounded shadow" alt="\u041e\u0431\u043b\u043e\u0436\u043a\u0430">{% else %}<div class="bg-light border rounded p-5 text-center text-muted">\u041d\u0435\u0442 \u043e\u0431\u043b\u043e\u0436\u043a\u0438</div>{% endif %}</div>
<div class="col-md-8"><h1>{{ book.title }}</h1><p class="text-muted">{{ book.author }}, {{ book.year }}</p>
<p><strong>\u0418\u0437\u0434\u0430\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e:</strong> {{ book.publisher }}</p>
<p><strong>\u041e\u0431\u044a\u0451\u043c:</strong> {{ book.pages_volume }} \u0441\u0442\u0440.</p>
<p><strong>\u0416\u0430\u043d\u0440\u044b:</strong> {% if book.genres %}{{ book.genre_names }}{% else %}\u2014{% endif %}</p>
<div class="book-description mt-3">{{ book.description_html | safe }}</div>
{% if user and user.role_name == 'user' %}
<button type="button" class="btn btn-outline-primary mt-3" data-bs-toggle="modal" data-bs-target="#addToCollectionModal">\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0443</button>
{% endif %}
</div></div>
<hr class="my-4"><h3>\u0420\u0435\u0446\u0435\u043d\u0437\u0438\u0438</h3>
{% if reviews %}{% for review in reviews %}<div class="card mb-3"><div class="card-body">
<div class="d-flex justify-content-between"><strong>{{ review.author_name }}</strong><span class="badge bg-primary">{{ review.rating }}/5</span></div>
<small class="text-muted">{{ review.created_at.strftime('%d.%m.%Y %H:%M') if review.created_at else '' }}</small>
<div class="mt-2">{{ review.text_html | safe }}</div></div></div>{% endfor %}{% else %}<p class="text-muted">\u0420\u0435\u0446\u0435\u043d\u0437\u0438\u0439 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442.</p>{% endif %}
{% if user and user.role_name in ['admin', 'moderator', 'user'] %}
{% if user_review %}<div class="card border-success mt-4"><div class="card-header">\u0412\u0430\u0448\u0430 \u0440\u0435\u0446\u0435\u043d\u0437\u0438\u044f</div><div class="card-body">
<span class="badge bg-success mb-2">{{ user_review.rating }}/5</span><div>{{ user_review.text_html | safe }}</div></div></div>
{% else %}<div class="mt-4"><a href="{{ url_for('reviews.add', book_id=book.id) }}" class="btn btn-success">\u041d\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u0440\u0435\u0446\u0435\u043d\u0437\u0438\u044e</a></div>{% endif %}{% endif %}
{% if user and user.role_name == 'user' %}
<div class="modal fade" id="addToCollectionModal" tabindex="-1"><div class="modal-dialog"><div class="modal-content">
<div class="modal-header"><h5 class="modal-title">\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0432 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0443</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
<form method="POST" action="{{ url_for('collections.add_book_to_collection', book_id=book.id) }}"><div class="modal-body">
{% if user_collections %}<select class="form-select" name="collection_id" required>{% for c in user_collections %}<option value="{{ c.id }}">{{ c.name }}</option>{% endfor %}</select>
{% else %}<p class="text-muted mb-0">\u0423 \u0432\u0430\u0441 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442 \u043f\u043e\u0434\u0431\u043e\u0440\u043e\u043a. \u0421\u043e\u0437\u0434\u0430\u0439\u0442\u0435 \u0438\u0445 \u0432 \u0440\u0430\u0437\u0434\u0435\u043b\u0435 \u00ab\u041c\u043e\u0438 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0438\u00bb.</p>{% endif %}
</div><div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">\u041e\u0442\u043c\u0435\u043d\u0430</button>{% if user_collections %}<button type="submit" class="btn btn-primary">\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c</button>{% endif %}</div></form>
</div></div></div>{% endif %}
{% endblock %}
""",
    )

    write(
        "reviews/form.html",
        f"""{{% extends "base.html" %}}
{{% block title %}}\u041d\u043e\u0432\u0430\u044f \u0440\u0435\u0446\u0435\u043d\u0437\u0438\u044f \u2014 {{{{ book.title }}}}{{% endblock %}}
{{% block extra_css %}}{easymde_css}{{% endblock %}}
{{% block content %}}
<h1 class="mb-4">\u0420\u0435\u0446\u0435\u043d\u0437\u0438\u044f \u043d\u0430 \u00ab{{{{ book.title }}}}\u00bb</h1>
<form method="POST">
<div class="mb-3"><label for="rating" class="form-label">\u041e\u0446\u0435\u043d\u043a\u0430</label>
<select class="form-select" id="rating" name="rating">
{{% for value, label in rating_labels.items()|sort(reverse=true) %}}
<option value="{{{{ value }}}}" {{% if form_data.rating|string == value|string %}}selected{{% elif value == 5 and not form_data.rating %}}selected{{% endif %}}>{{{{ label }}}}</option>
{{% endfor %}}</select></div>
<div class="mb-3"><label for="text" class="form-label">\u0422\u0435\u043a\u0441\u0442 \u0440\u0435\u0446\u0435\u043d\u0437\u0438\u0438</label><textarea class="form-control" id="text" name="text" rows="8">{{{{ form_data.text or '' }}}}</textarea></div>
<button type="submit" class="btn btn-primary">\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c</button>
<a href="{{{{ url_for('books.view', book_id=book.id) }}}}" class="btn btn-secondary">\u041e\u0442\u043c\u0435\u043d\u0430</a>
</form>{{% endblock %}}
{{% block extra_js %}}{easymde_js}<script>
const easyMDE = new EasyMDE({{element: document.getElementById('text'), spellChecker: false, status: false}});
document.querySelector('form').addEventListener('submit', () => easyMDE.codemirror.save());
</script>{{% endblock %}}
""",
    )

    write(
        "collections/list.html",
        """{% extends "base.html" %}
{% block title %}\u041c\u043e\u0438 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0438 \u2014 \u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430{% endblock %}
{% block content %}
<h1 class="mb-4">\u041c\u043e\u0438 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0438</h1>
{% if collections %}
<table class="table table-striped"><thead><tr><th>\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435</th><th>\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u043d\u0438\u0433</th><th></th></tr></thead><tbody>
{% for collection in collections %}<tr><td>{{ collection.name }}</td><td>{{ collection.book_count }}</td>
<td><a href="{{ url_for('collections.view', collection_id=collection.id) }}" class="btn btn-sm btn-outline-primary">\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440</a></td></tr>{% endfor %}
</tbody></table>{% else %}<p class="text-muted">\u041f\u043e\u0434\u0431\u043e\u0440\u043e\u043a \u043f\u043e\u043a\u0430 \u043d\u0435\u0442.</p>{% endif %}
<button type="button" class="btn btn-success mt-3" data-bs-toggle="modal" data-bs-target="#newCollectionModal">\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0443</button>
<div class="modal fade" id="newCollectionModal" tabindex="-1"><div class="modal-dialog"><div class="modal-content">
<div class="modal-header"><h5 class="modal-title">\u041d\u043e\u0432\u0430\u044f \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0430</h5><button type="button" class="btn-close" data-bs-dismiss="modal"></button></div>
<form method="POST" action="{{ url_for('collections.add') }}"><div class="modal-body">
<label for="name" class="form-label">\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0438</label>
<input type="text" class="form-control" id="name" name="name" required></div>
<div class="modal-footer"><button type="button" class="btn btn-secondary" data-bs-dismiss="modal">\u041e\u0442\u043c\u0435\u043d\u0430</button><button type="submit" class="btn btn-primary">\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c</button></div></form>
</div></div></div>
{% endblock %}
""",
    )

    write(
        "collections/view.html",
        """{% extends "base.html" %}
{% block title %}{{ collection.name }} \u2014 \u041c\u043e\u0438 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0438{% endblock %}
{% block content %}
<h1 class="mb-4">{{ collection.name }}</h1>
<a href="{{ url_for('collections.index') }}" class="btn btn-link ps-0 mb-3">&larr; \u041a \u0441\u043f\u0438\u0441\u043a\u0443 \u043f\u043e\u0434\u0431\u043e\u0440\u043e\u043a</a>
{% if books %}<div class="list-group">{% for book in books %}
<a href="{{ url_for('books.view', book_id=book.id) }}" class="list-group-item list-group-item-action">
<div class="d-flex w-100 justify-content-between"><h5 class="mb-1">{{ book.title }}</h5><small>{{ book.year }}</small></div>
<p class="mb-1 text-muted">{{ book.author }}</p></a>{% endfor %}</div>
{% else %}<p class="text-muted">\u0412 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0435 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442 \u043a\u043d\u0438\u0433.</p>{% endif %}
{% endblock %}
""",
    )

    write(
        "base.html",
        """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430{% endblock %}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
{% block extra_css %}{% endblock %}
</head>
<body class="d-flex flex-column min-vh-100">
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
<div class="container">
<a class="navbar-brand" href="{{ url_for('books.index') }}">\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u0430\u044f \u0431\u0438\u0431\u043b\u0438\u043e\u0442\u0435\u043a\u0430</a>
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"><span class="navbar-toggler-icon"></span></button>
<div class="collapse navbar-collapse" id="navbarNav">
<ul class="navbar-nav me-auto">
<li class="nav-item"><a class="nav-link" href="{{ url_for('books.index') }}">\u0413\u043b\u0430\u0432\u043d\u0430\u044f</a></li>
{% if current_user and current_user.role_name == 'user' %}
<li class="nav-item"><a class="nav-link" href="{{ url_for('collections.index') }}">\u041c\u043e\u0438 \u043f\u043e\u0434\u0431\u043e\u0440\u043a\u0438</a></li>
{% endif %}
</ul>
<ul class="navbar-nav">
{% if current_user %}
<li class="nav-item"><span class="navbar-text text-white me-3">{{ current_user.last_name }} {{ current_user.first_name }}{% if current_user.middle_name %} {{ current_user.middle_name }}{% endif %}</span></li>
<li class="nav-item"><a class="btn btn-outline-light btn-sm" href="{{ url_for('auth.logout', next=request.path) }}">\u0412\u044b\u0439\u0442\u0438</a></li>
{% else %}
<li class="nav-item"><a class="btn btn-outline-light btn-sm" href="{{ url_for('auth.login') }}">\u0412\u043e\u0439\u0442\u0438</a></li>
{% endif %}
</ul></div></div></nav>
<main class="container flex-grow-1 py-4">
{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}{% for category, message in messages %}
<div class="alert alert-{{ category }} alert-dismissible fade show">{{ message }}<button type="button" class="btn-close" data-bs-dismiss="alert"></button></div>
{% endfor %}{% endif %}{% endwith %}
{% block content %}{% endblock %}
</main>
<footer class="bg-light py-3 mt-auto"><div class="container text-center text-muted">
<small>\u0413\u0440. 241-3211 \u041a\u043e\u043c\u0430\u0440 \u042f\u0440\u043e\u0441\u043b\u0430\u0432\u0430 \u0420\u0443\u0441\u043b\u0430\u043d\u043e\u0432\u043d\u0430</small>
</div></footer>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
{% block extra_js %}{% endblock %}
</body></html>
""",
    )


if __name__ == "__main__":
    main()
