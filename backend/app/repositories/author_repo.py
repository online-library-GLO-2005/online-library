from app.repositories.base_repo import BaseRepo
from app.models.author import Author


class AuthorRepo(BaseRepo):
    def get_all(self, search_name=None):
        query = f"SELECT * FROM {Author.TABLE}"
        params = []
        if search_name:
            query += f" WHERE {Author.Columns.NAME} LIKE %s"
            params.append(f"%{search_name}%")

        rows = self._db.execute(query, tuple(params))
        return [Author(id=r[Author.Columns.ID], name=r[Author.Columns.NAME],
                       description=r[Author.Columns.DESCRIPTION],
                       photo_url=r[Author.Columns.PHOTO_URL]) for r in rows] if rows else []

    def get_by_id(self, aid: int):
        query = f"SELECT * FROM {Author.TABLE} WHERE {Author.Columns.ID} = %s"
        rows = self._db.execute(query, (aid,))
        if rows:
            r = rows[0]
            return Author(id=r[Author.Columns.ID], name=r[Author.Columns.NAME],
                          description=r[Author.Columns.DESCRIPTION],
                          photo_url=r[Author.Columns.PHOTO_URL])
        return None

    def create(self, data: dict):
        query = f"""
            INSERT INTO {Author.TABLE} ({Author.Columns.NAME}, {Author.Columns.DESCRIPTION}, {Author.Columns.PHOTO_URL})
            VALUES (%s, %s, %s)
        """
        last_id = self._db.execute(query, (data['name'], data.get('description'), data.get('photo_url')),
                                   return_id=True)
        return self.get_by_id(last_id)

    def update(self, aid: int, data: dict):
        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {Author.TABLE} SET {set_clause} WHERE {Author.Columns.ID} = %s"
        params = list(data.values()) + [aid]
        self._db.execute(query, tuple(params))

    def delete(self, aid: int):
        query = f"DELETE FROM {Author.TABLE} WHERE {Author.Columns.ID} = %s"
        self._db.execute(query, (aid,))


author_repo = AuthorRepo()