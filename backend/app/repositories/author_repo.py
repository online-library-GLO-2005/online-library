from app.repositories.base_repo import BaseRepo
from app.models.author import Author

from app.models.book import Book


class AuthorRepo(BaseRepo):
    def get_all(self, search_name=None):
        query = f"SELECT * FROM {Author.TABLE}"
        params = []
        if search_name:
            query += f" WHERE {Author.Columns.NAME} LIKE %s"
            params.append(f"%{search_name}%")

        rows = self._db.execute(query, tuple(params))
        # Utilisation de la méthode de classe from_dict
        return [Author.from_dict(r) for r in rows] if rows else []

    def get_by_id(self, aid: int):
        query = f"SELECT * FROM {Author.TABLE} WHERE {Author.Columns.ID} = %s"
        rows = self._db.execute(query, (aid,))
        # Plus besoin de déplier r[Author.Columns.ID] manuellement
        return Author.from_dict(rows[0]) if rows else None

    def create(self, data: dict):
        # Ici on utilise les constantes de Columns pour être sûr de taper les bons noms SQL
        query = f"""
            INSERT INTO {Author.TABLE} ({Author.Columns.NAME}, {Author.Columns.DESCRIPTION}, {Author.Columns.PHOTO_URL})
            VALUES (%s, %s, %s)
        """
        params = (data['name'], data.get('description'), data.get('photo_url'))
        last_id = self._db.execute(query, params, return_id=True)
        return self.get_by_id(last_id)

    def update(self, aid: int, data: dict):
        # On s'assure que les clés du dictionnaire 'data' correspondent aux colonnes SQL
        # Si 'data' vient de Postman avec 'name', on doit le mapper vers 'nom'
        mapped_data = {}
        if 'name' in data: mapped_data[Author.Columns.NAME] = data['name']
        if 'description' in data: mapped_data[Author.Columns.DESCRIPTION] = data['description']
        if 'photo_url' in data: mapped_data[Author.Columns.PHOTO_URL] = data['photo_url']

        if not mapped_data:
            return

        set_clause = ", ".join([f"{k} = %s" for k in mapped_data.keys()])
        query = f"UPDATE {Author.TABLE} SET {set_clause} WHERE {Author.Columns.ID} = %s"
        params = list(mapped_data.values()) + [aid]
        self._db.execute(query, tuple(params))

    def delete(self, aid: int):
        query = f"DELETE FROM {Author.TABLE} WHERE {Author.Columns.ID} = %s"
        self._db.execute(query, (aid,))

    def get_books_by_author(self, aid: int):
        query = """
            SELECT l.* FROM Livre l
            JOIN Ecrit e ON l.LID = e.LID
            WHERE e.AID = %s
        """
        rows = self._db.execute(query, (aid,))
        # Transformation en objets Book pour que le Schema les reconnaisse
        return [Book.from_dict(row) for row in rows] if rows else []

author_repo = AuthorRepo()