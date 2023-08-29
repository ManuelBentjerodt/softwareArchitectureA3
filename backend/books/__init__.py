from flask import Flask
from flask import render_template, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_alembic import Alembic
from .db import db
from books.models import Author, Book
from itertools import chain

import os
from dotenv import load_dotenv
import pathlib

dotenv_path = pathlib.Path('../../..') / '.env'
load_dotenv(dotenv_path=dotenv_path)

DB_URL = os.getenv("DB_URL")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PROTOCOL = os.getenv("DB_PROTOCOL")
print(DB_PROTOCOL)
DB_STRING_CONNECTION = f"{DB_PROTOCOL}://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}"



def create_app():
    # create and configure the app
    app = Flask(__name__)
    
    
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_STRING_CONNECTION
    alembic = Alembic()

    db.init_app(app)
    alembic.init_app(app)

    import books.models

    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    # a simple page that says hello
    @app.route('/')
    def base():
        return render_template('index.html')

    @app.route('/authors')
    def authors_index():
        authors = db.session.execute(db.select(Author)).scalars()
        authors_dicts = []
        for author in authors:
            ratings = list(chain(*list(map(lambda x: x.ratings, author.books))))
            print(ratings)
            authors_dicts.append({
                'item': author,
                'average_score': 0 if len(ratings) == 0 else sum(map(lambda x: x.score, ratings)) / len(ratings)
            })
        return render_template('authors.html', authors=authors_dicts)
    
    @app.route('/books')
    def books_index():
        books = db.session.execute(db.select(Book)).scalars()
        books_dicts = []
        for book in books:
            books_dicts.append({
                'item': book,
                'average_score': 0 if len(book.ratings) == 0 else sum(map(lambda x: x.score, book.ratings))/len(book.ratings)
            })
        return render_template('books.html', books=books_dicts)

    return app
