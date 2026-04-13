from app.repositories.base_repo import BaseRepo
from app.models.comment import Comment

class CommentRepo(BaseRepo):
    def get_by_id(self, comment_id: int) -> Comment | None:
        query = f"SELECT * FROM {Comment.TABLE} WHERE {Comment.Columns.ID} = %s"
        rows = self._db.execute(query, (comment_id,))
        return Comment(**rows[0]) if rows else None

    def create(self, user_id, book_id, message):
        query = f"""
            INSERT INTO {Comment.TABLE} ({Comment.Columns.UID}, {Comment.Columns.LID}, {Comment.Columns.MESSAGE})
            VALUES (%s, %s, %s)
        """
        last_id = self._db.execute(query, (user_id, book_id, message), return_id=True)
        return self.get_by_id(last_id)

    def update(self, comment_id, new_message):
        query = f"UPDATE {Comment.TABLE} SET {Comment.Columns.MESSAGE} = %s WHERE {Comment.Columns.ID} = %s"
        self._db.execute(query, (new_message, comment_id))

    def delete(self, comment_id):
        query = f"DELETE FROM {Comment.TABLE} WHERE {Comment.Columns.ID} = %s"
        self._db.execute(query, (comment_id,))

comment_repo = CommentRepo()