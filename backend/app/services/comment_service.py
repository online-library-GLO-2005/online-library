from app.services.ownable_service import OwnableService
from app.repositories.comment_repo import comment_repo
from app.errors import AppError

class CommentService(OwnableService):
    def __init__(self):
        self._repo = comment_repo

    def get_owner_id(self, resource_id) -> str:
        comment = self._repo.get_by_id(resource_id)
        if not comment:
            raise AppError("Commentaire introuvable", 404)
        return str(comment.user_id)

    def add_comment(self, user_id, book_id, message):
        return self._repo.create(user_id, book_id, message)

    def update_comment(self, comment_id, message):
        self._repo.update(comment_id, message)
        return self._repo.get_by_id(comment_id)

    def delete_comment(self, comment_id):
        self._repo.delete(comment_id)

    def get_comments_by_book(self, lid: int):
        return self._repo.get_by_book(lid)

comment_service = CommentService()