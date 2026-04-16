from app.repositories.rating_repo import RatingRepo

from app.utils.apiResponse import error_response


class RatingService:
    def __init__(self):
        self._repo = RatingRepo()

    def rate_book(self, user_id, book_id, note):
        if not (0 <= note <= 5):
            error_response(400, "La note doit être comprise entre 0 et 5")

        return self._repo.upsert_rating(user_id, book_id, note)


rating_service = RatingService()