from app.repositories.base_repo import BaseRepo
from app.models.comment import Comment

class CommentRepo(BaseRepo):
    def get_by_id(self, comment_id: int) -> Comment | None:
        # On fait une jointure avec la table Utilisateur pour récupérer le nom
        query = f"""
            SELECT c.*, u.nom as user_name 
            FROM {Comment.TABLE} c
            JOIN Utilisateur u ON c.UID = u.UID
            WHERE c.{Comment.Columns.ID} = %s
        """
        rows = self._db.execute(query, (comment_id,))
        return Comment.from_dict(rows[0]) if rows else None

    def get_by_book(self, book_id: int):
        # jointure pour avoir le nom de l'auteur du commentaire
        query = """
            SELECT c.*, u.nom as user_name 
            FROM Commentaire c
            JOIN Utilisateur u ON c.UID = u.UID
            WHERE c.LID = %s
            ORDER BY c.date_publication DESC
        """
        rows = self._db.execute(query, (book_id,))
        return [Comment.from_dict(r) for r in rows] if rows else []

    # La méthode create reste identique, car elle appelle get_by_id à la fin
    def create(self, user_id, book_id, message):
        query = f"""
            INSERT INTO {Comment.TABLE} 
            ({Comment.Columns.UID}, {Comment.Columns.LID}, {Comment.Columns.MESSAGE})
            VALUES (%s, %s, %s)
        """
        last_id = self._db.execute(query, (user_id, book_id, message), return_id=True)
        # get_by_id retournera maintenant l'objet avec le user_name inclus !
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