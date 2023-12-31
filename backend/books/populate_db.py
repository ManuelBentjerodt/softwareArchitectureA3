import csv
import sys
sys.path.append('/home/ec2-user/softwareArchitectureA3/backend')

from books.models import Author, Book, Rating
from books.db import db
from books import create_app

def load_authors():
    with open('database_files/authors.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            author = Author(name=row['name'], openlibrary_key=row['key'])
            db.session.add(author)
    db.session.commit()

def load_books():
    with open('database_files/books.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            author = db.session.query(Author).filter_by(openlibrary_key=row['author']).first()
            if author:
                book = Book(title=row['title'], openlibrary_key=row['key'], author=author, description=row.get('description', ''))
                db.session.add(book)
    db.session.commit()

def load_ratings():
    with open('database_files/ratings.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            book = db.session.query(Book).filter_by(openlibrary_key=row['work']).first()
            if book:
                rating = Rating(book=book, score=int(row['score']))
                db.session.add(rating)
    db.session.commit()

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        load_authors()
        load_books()
        load_ratings()

