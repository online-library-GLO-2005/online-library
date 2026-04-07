from backend.app.errors import AppError
from app.repositories.base_repo import BaseRepo


class BookRepo(BaseRepo):
    def get_all_books(self):
        pass

    def create_book(self, title, author_id):
        pass
