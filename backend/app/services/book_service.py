from app.repositories.book_repo import book_repo
from .ownable_service import OwnableService
from app.errors import AppError


class BookService:
    def __init__(self):
        self._repo = book_repo

    # Add book: if title is the same as another put a (index number)
    # Be careful of racing conditions
    def insert_book(self, title, author_id=None):
        pass

    def get_books(self):
        pass


book_service = BookService()
