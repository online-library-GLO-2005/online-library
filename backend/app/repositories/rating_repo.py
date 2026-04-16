from app.repositories.base_repo import BaseRepo


class RatingRepo(BaseRepo):
    def upsert_rating(self, user_id, book_id, note):
        query = """
            INSERT INTO Noter (UID, LID, note)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE note = VALUES(note)
        """
        self._db.execute(query, (user_id, book_id, note))
        return True

    def get_average_rating(self, book_id):
        query = "SELECT AVG(note) as average FROM Noter WHERE LID = %s"
        result = self._db.execute(query, (book_id,))
        return result[0]['average'] if result else 0