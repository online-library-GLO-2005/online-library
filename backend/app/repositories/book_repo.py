from app.repositories.base_repo import BaseRepo
from app.models.book import Book

from app.models.author import Author

from app.models.genre import Genre


class BookRepo(BaseRepo):
    def get_all_books(self):
        query = f"SELECT * FROM {Book.TABLE}"
        rows = self._db.execute(query)
        # MODIFICATION : Utilisation de from_dict au lieu de **row
        return [Book.from_dict(row) for row in rows] if rows else []

    def get_by_id(self, book_id: int) -> Book | None:
        query = f"SELECT * FROM {Book.TABLE} WHERE {Book.Columns.ID} = %s"
        rows = self._db.execute(query, (book_id,))
        # MODIFICATION : Utilisation de from_dict ici aussi
        return Book.from_dict(rows[0]) if rows else None

    def create_book(self, data: dict):
        check_query = f"SELECT COUNT(*) as count FROM {Book.TABLE} WHERE {Book.Columns.TITLE} LIKE %s"
        result = self._db.execute(check_query, (f"{data['title']}%",))
        count = result[0]['count']

        final_title = data['title'] if count == 0 else f"{data['title']} ({count})"

        insert_query = f"""
            INSERT INTO {Book.TABLE} 
            ({Book.Columns.EID}, {Book.Columns.ISBN}, {Book.Columns.TITLE}, 
             {Book.Columns.DESCRIPTION}, {Book.Columns.COVER_URL}, 
             {Book.Columns.CONTENT_URL}, {Book.Columns.PUB_DATE})
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data['eid'], data['isbn'], final_title,
            data.get('description'), data.get('cover_url'),
            data.get('content_url'), data['pub_date']
        )

        last_id = self._db.execute(insert_query, params, return_id=True)
        return self.get_by_id(last_id)

    def update_fields(self, book_id: int, fields_dict: dict):
        set_clause = ", ".join([f"{col} = %s" for col in fields_dict.keys()])
        query = f"UPDATE {Book.TABLE} SET {set_clause} WHERE {Book.Columns.ID} = %s"

        params = list(fields_dict.values())
        params.append(book_id)

        self._db.execute(query, tuple(params))

    def link_author(self, lid: int, aid: int):
        query = "INSERT INTO Ecrit (LID, AID) VALUES (%s, %s)"
        return self._db.execute(query, (lid, aid))

    def link_genre(self, lid: int, gid: int):
        query = "INSERT INTO Classer (LID, GID) VALUES (%s, %s)"
        return self._db.execute(query, (lid, gid))

    def get_authors_by_book(self, lid: int):
        query = """
            SELECT a.* FROM Auteur a
            JOIN Ecrit e ON a.AID = e.AID
            WHERE e.LID = %s
        """
        return self._db.execute(query, (lid,))

    def get_genres_by_book(self, lid: int):
        query = """
            SELECT g.* FROM Genre g
            JOIN Classer c ON g.GID = c.GID
            WHERE c.LID = %s
        """
        return self._db.execute(query, (lid,))

    def get_authors_for_book(self, lid: int):
        # La table de liaison est "Ecrit" (AID, LID)
        query = """
            SELECT a.* FROM Auteur a
            JOIN Ecrit e ON a.AID = e.AID
            WHERE e.LID = %s
        """
        rows = self._db.execute(query, (lid,))
        return [Author.from_dict(row) for row in rows]

    def get_genres_for_book(self, lid: int):
        # La table de liaison est "Classer" (GID, LID)
        query = """
            SELECT g.* FROM Genre g
            JOIN Classer c ON g.GID = c.GID
            WHERE c.LID = %s
        """
        rows = self._db.execute(query, (lid,))
        return [Genre.from_dict(row) for row in rows]

book_repo = BookRepo()