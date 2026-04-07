from app.repositories.book_repo import BookRepo

# from app.repositories.book_repo import get_all_books, create_book


class BookService:
    def __init__(self, repo: BookRepo):
        self._repo = repo

    # Add book: if title is the same as another put a (index number)
    # Be careful of racing conditions
    def insert_book(self, title, author_id=None):
        pass

    def get_books(self):
        pass
