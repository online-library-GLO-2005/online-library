from app.repositories.book_repo import get_all_books, create_book

def insert_book(title, author_id=None):
    return create_book(title, author_id)

def get_books():
    return get_all_books()