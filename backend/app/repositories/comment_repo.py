from app.repositories.base_repo import BaseRepo
from app.models.comment import Comment

class CommentRepo(BaseRepo):
    def get_by_id(self, comment_id: int) -> Comment | None:
        query = f"SELECT * FROM {Comment.TABLE} WHERE {Comment.Columns.ID} = %s"
        rows = self._db.execute(query, (comment_id,))
        return Comment.from_dict(rows[0]) if rows else None

    def get_by_book(self, book_id: int):
        rows = self._db.execute("SELECT * FROM Commentaire WHERE LID = 1")
        return [Comment.from_dict(r) for r in rows] if rows else []

    def create(self, user_id, book_id, message):
        query = f"""
            INSERT INTO {Comment.TABLE} 
            ({Comment.Columns.UID}, {Comment.Columns.LID}, {Comment.Columns.MESSAGE})
            VALUES (%s, %s, %s)
        """
        # On utilise return_id=True pour récupérer le CID (Comment ID) auto-généré
        last_id = self._db.execute(query, (user_id, book_id, message), return_id=True)
        return self.get_by_id(last_id)

    def update(self, comment_id, new_message):
        query = f"""
            UPDATE {Comment.TABLE} 
            SET {Comment.Columns.MESSAGE} = %s 
            WHERE {Comment.Columns.ID} = %s
        """
        self._db.execute(query, (new_message, comment_id))
        return self.get_by_id(comment_id)

    def delete(self, comment_id):
        query = f"DELETE FROM {Comment.TABLE} WHERE {Comment.Columns.ID} = %s"
        self._db.execute(query, (comment_id,))


comment_repo = CommentRepo()