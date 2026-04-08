from app.repositories.base_repo import BaseRepo
from app.models.book import Book


class BookRepo(BaseRepo):
    def get_all_books(self):
        pass

    def create_book(self, title, author_id):
        pass

    # This code is not complete (colomns not all there)
    # Merely an example of utilisation of Models
    def get_by_id(self, book_id: str) -> Book | None:
        query = f"""
            SELECT {Book.Columns.ID}, 
                {Book.Columns.TITLE}, 
                {Book.Columns.ISBN}
            FROM {Book.TABLE}
            WHERE {Book.Columns.ID} = %s
        """

        rows = self._db.execute(query, (book_id,))
        if not rows:
            return None
        row = rows[0]
        return Book(
            id=row[Book.Columns.ID],
            title=row[Book.Columns.TITLE],
            isbn=row[Book.Columns.ISBN],
        )


book_repo = BookRepo()
