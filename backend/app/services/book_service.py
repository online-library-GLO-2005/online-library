from app.repositories.book_repo import book_repo
from app.errors import AppError
from ..models.book import Book
from ..schemas.book_schema import BookSchema


class BookService:
    def __init__(self):
        self._repo = book_repo

    def get_books(self):
        return self._repo.get_all_books()

    def insert_book(self, book_data: dict):
        return self._repo.create_book(book_data)

    def get_book_by_id(self, book_id: int):
        book = self._repo.get_by_id(book_id)
        if not book:
            raise AppError(f"Livre {book_id} introuvable", 404)
        return book

    def get_book_details(self, lid: int):
        book = self.get_book_by_id(lid)

        authors_data = self._repo.get_authors_by_book(lid)
        genres_data = self._repo.get_genres_by_book(lid)

        book_dict = BookSchema().dump(book)
        book_dict["authors"] = authors_data
        book_dict["genres"] = genres_data

        return book_dict

    def add_book_with_relations(self, data: dict, author_ids: list, genre_ids: list):
        new_book = self._repo.create_book(data)
        lid = new_book.id

        for aid in author_ids:
            self._repo.link_author(lid, aid)
        for gid in genre_ids:
            self._repo.link_genre(lid, gid)

        return self.get_book_details(lid)

    def link_author(self, book_id: int, author_id: int):
        book = self.get_book_by_id(book_id)  # Ensure book exists
        if not book:
            raise AppError(404, "Livre introuvable")

        self._repo.link_author(book_id, author_id)

    def link_genre(self, book_id: int, genre_id: int):
        book = self.get_book_by_id(book_id)  # Ensure book exists
        if not book:
            raise AppError(404, "Livre introuvable")
        self._repo.link_genre(book_id, genre_id)

    def update_book_media(
        self, book_id: int, cover_url: str = None, content_url: str = None
    ):
        book = self.get_book_by_id(book_id)
        if not book:
            raise AppError(404, "Livre introuvable")

        updates = {}
        if cover_url:
            updates[Book.Columns.COVER_URL] = cover_url
        if content_url:
            updates[Book.Columns.CONTENT_URL] = content_url

        if updates:
            self._repo.update_fields(book_id, updates)

        return self._repo.get_by_id(book_id)

    def get_authors_by_book(self, lid: int):
        return self._repo.get_authors_for_book(lid)

    def get_genres_by_book(self, lid: int):
        return self._repo.get_genres_for_book(lid)




book_service = BookService()
