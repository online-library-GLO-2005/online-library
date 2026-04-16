from app.repositories.base_repo import BaseRepo
from app.models.user import User
from app.models.book import Book


class UserRepo(BaseRepo):
    def get_by_id(self, uid: int) -> User | None:
        query = f"SELECT * FROM {User.TABLE} WHERE {User.Columns.ID} = %s"
        rows = self._db.execute(query, (uid,))
        return User.from_dict(rows[0]) if rows else None

    def get_all(self):
        query = f"SELECT * FROM {User.TABLE}"
        rows = self._db.execute(query)
        return [User.from_dict(r) for r in rows] if rows else []

    def update(self, uid: int, data: dict):
        set_clause = ", ".join([f"{k} = %s" for k in data.keys()])
        query = f"UPDATE {User.TABLE} SET {set_clause} WHERE {User.Columns.ID} = %s"
        params = list(data.values()) + [uid]
        self._db.execute(query, tuple(params))
        return self.get_by_id(uid)

    def delete(self, uid: int):
        query = f"DELETE FROM {User.TABLE} WHERE {User.Columns.ID} = %s"
        self._db.execute(query, (uid,))

    def get_consulted_books(self, uid: int):
        query = f"""
            SELECT l.* FROM Livre l
            JOIN Consulter c ON l.LID = c.LID
            WHERE c.UID = %s
            ORDER BY c.date_consultation DESC
        """
        rows = self._db.execute(query, (uid,))
        return [Book.from_dict(r) for r in rows] if rows else []

    def get_favorite_books(self, uid: int):
        query = f"""
            SELECT l.* FROM Livre l
            JOIN Suit s ON l.LID = s.LID
            WHERE s.UID = %s AND s.favoris = TRUE
        """
        rows = self._db.execute(query, (uid,))
        return [Book.from_dict(r) for r in rows] if rows else []

    def add_to_favorites(self, uid: int, lid: int):
        query = f"""
            INSERT INTO Suit (UID, LID, favoris) VALUES (%s, %s, TRUE)
            ON DUPLICATE KEY UPDATE favoris = TRUE
        """
        self._db.execute(query, (uid, lid))

    def remove_from_favorites(self, uid: int, lid: int):
        query = "UPDATE Suit SET favoris = FALSE WHERE UID = %s AND LID = %s"
        self._db.execute(query, (uid, lid))

    def get_user_comments(self, uid: int):
        query = "SELECT * FROM Commentaire WHERE UID = %s"
        return self._db.execute(query, (uid,))

    def is_admin(self, uid: int) -> bool:
        query = f"""
            SELECT 1
            FROM {User.Admin_TABLE}
            WHERE {User.Columns.ID} = %s
        """
        rows = self._db.execute(query, (uid,))
        return bool(rows)

    def get_all_users(self):
        query = f"SELECT * FROM {User.TABLE}"
        rows = self._db.execute(query)
        return [User.from_dict(r) for r in rows] if rows else []




user_repo = UserRepo()
