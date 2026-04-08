from .ownable_service import OwnableService
from app.repositories.comment_repo import comment_repo


class CommentService(OwnableService):
    def __init__(self):
        self._repo = comment_repo

    # TO BE IMPLEMENTED (important for guard)
    # type: ignore[override]
    def get_owner_id(self, resource_id) -> str:
        raise NotImplemented


comment_service = CommentService()
