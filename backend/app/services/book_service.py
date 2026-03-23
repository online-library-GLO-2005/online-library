from repositories.book_repo import get_all_books, create_book
from utils.errors import AppError

def list_books():
    return get_all_books()

def add_book(data):
    if "title" not in data:
        raise AppError("Title is required")
    return create_book(data)