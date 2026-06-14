from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


book_genres = db.Table(
    "book_genres",
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)


collection_books = db.Table(
    "collection_books",
    db.Column("collection_id", db.Integer, db.ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
)


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)

    users = db.relationship("User", back_populates="role", cascade="all, delete-orphan")

    def __str__(self):
        return self.name


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)

    role = db.relationship("Role", back_populates="users")
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    collections = db.relationship("Collection", back_populates="user", cascade="all, delete-orphan")

    @property
    def role_name(self):
        return self.role.name if self.role else None

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        return " ".join(parts)

    def __str__(self):
        return self.login


class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    pages_volume = db.Column(db.Integer, nullable=False)

    genres = db.relationship(
        "Genre",
        secondary=book_genres,
        lazy="select",
        backref=db.backref("books", lazy="select"),
    )
    cover = db.relationship("Cover", uselist=False, back_populates="book", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="book", cascade="all, delete-orphan")
    collections = db.relationship(
        "Collection",
        secondary=collection_books,
        back_populates="books",
        lazy="select",
    )

    @property
    def review_count(self):
        return len(self.reviews)

    @property
    def avg_rating(self):
        if not self.reviews:
            return 0
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 1)

    @property
    def genre_names(self):
        return ", ".join(genre.name for genre in sorted(self.genres, key=lambda g: g.name))


class Cover(db.Model):
    __tablename__ = "covers"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5_hash = db.Column(db.String(32), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), unique=True, nullable=False)

    book = db.relationship("Book", back_populates="cover")


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    book = db.relationship("Book", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    @property
    def author_name(self):
        return self.user.full_name if self.user else ""


class Collection(db.Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", back_populates="collections")
    books = db.relationship(
        "Book",
        secondary=collection_books,
        back_populates="collections",
        lazy="select",
    )
