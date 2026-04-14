from app.repositories.base_repo import BaseRepo
from app.models.genre import Genre

class GenreRepo(BaseRepo):
    def get_all(self):
        query = f"SELECT * FROM {Genre.TABLE}"
        rows = self._db.execute(query)
        # MODIFICATION : Utilisation de la liste de compréhension avec from_dict
        return [Genre.from_dict(r) for r in rows] if rows else []

    def get_by_id(self, gid: int):
        query = f"SELECT * FROM {Genre.TABLE} WHERE {Genre.Columns.ID} = %s"
        rows = self._db.execute(query, (gid,))
        # MODIFICATION : Utilisation directe de from_dict
        return Genre.from_dict(rows[0]) if rows else None

    def create(self, name: str):
        query = f"INSERT INTO {Genre.TABLE} ({Genre.Columns.NAME}) VALUES (%s)"
        last_id = self._db.execute(query, (name,), return_id=True)
        return self.get_by_id(last_id)

    def update(self, gid: int, name: str):
        query = f"UPDATE {Genre.TABLE} SET {Genre.Columns.NAME} = %s WHERE {Genre.Columns.ID} = %s"
        self._db.execute(query, (name, gid))
        # Optionnel : On peut retourner l'objet mis à jour
        return self.get_by_id(gid)

    def delete(self, gid: int):
        query = f"DELETE FROM {Genre.TABLE} WHERE {Genre.Columns.ID} = %s"
        self._db.execute(query, (gid,))

genre_repo = GenreRepo()