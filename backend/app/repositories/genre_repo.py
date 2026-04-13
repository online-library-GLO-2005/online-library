from app.repositories.base_repo import BaseRepo
from app.models.genre import Genre

class GenreRepo(BaseRepo):
    def get_all(self):
        query = f"SELECT * FROM {Genre.TABLE}"
        rows = self._db.execute(query)
        return [Genre(id=r[Genre.Columns.ID], name=r[Genre.Columns.NAME]) for r in rows] if rows else []

    def get_by_id(self, gid: int):
        query = f"SELECT * FROM {Genre.TABLE} WHERE {Genre.Columns.ID} = %s"
        rows = self._db.execute(query, (gid,))
        if rows:
            r = rows[0]
            return Genre(id=r[Genre.Columns.ID], name=r[Genre.Columns.NAME])
        return None

    def create(self, name: str):
        query = f"INSERT INTO {Genre.TABLE} ({Genre.Columns.NAME}) VALUES (%s)"
        last_id = self._db.execute(query, (name,), return_id=True)
        return self.get_by_id(last_id)

    def update(self, gid: int, name: str):
        query = f"UPDATE {Genre.TABLE} SET {Genre.Columns.NAME} = %s WHERE {Genre.Columns.ID} = %s"
        self._db.execute(query, (name, gid))

    def delete(self, gid: int):
        query = f"DELETE FROM {Genre.TABLE} WHERE {Genre.Columns.ID} = %s"
        self._db.execute(query, (gid,))

genre_repo = GenreRepo()