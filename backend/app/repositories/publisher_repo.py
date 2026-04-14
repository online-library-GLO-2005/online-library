from app.repositories.base_repo import BaseRepo
from app.models.publisher import Publisher

class PublisherRepo(BaseRepo):
    def get_all(self):
        query = f"SELECT * FROM {Publisher.TABLE}"
        rows = self._db.execute(query)
        # On délègue la création de la liste au modèle
        return [Publisher.from_dict(r) for r in rows] if rows else []

    def get_by_id(self, eid: int):
        query = f"SELECT * FROM {Publisher.TABLE} WHERE {Publisher.Columns.ID} = %s"
        rows = self._db.execute(query, (eid,))
        # Plus besoin de déplier les champs un à un ici non plus
        return Publisher.from_dict(rows[0]) if rows else None

    def create(self, name: str, description: str = None):
        query = f"INSERT INTO {Publisher.TABLE} ({Publisher.Columns.NAME}, {Publisher.Columns.DESCRIPTION}) VALUES (%s, %s)"
        last_id = self._db.execute(query, (name, description), return_id=True)
        return self.get_by_id(last_id)

    def update(self, eid: int, name: str, description: str = None):
        query = f"""
            UPDATE {Publisher.TABLE} 
            SET {Publisher.Columns.NAME} = %s, {Publisher.Columns.DESCRIPTION} = %s 
            WHERE {Publisher.Columns.ID} = %s
        """
        self._db.execute(query, (name, description, eid))
        return self.get_by_id(eid)

    def delete(self, eid: int):
        query = f"DELETE FROM {Publisher.TABLE} WHERE {Publisher.Columns.ID} = %s"
        self._db.execute(query, (eid,))

publisher_repo = PublisherRepo()