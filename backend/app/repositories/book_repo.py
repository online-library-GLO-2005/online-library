from extensions import db
from models.book import Book

def get_all_books():
    return Book.query.all()

def create_book(data):
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return book