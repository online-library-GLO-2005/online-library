from .ownable_service import OwnableService
from app.repositories.user_repo import user_repo


class UserService(OwnableService):
    def __init__(self):
        self._repo = user_repo

    # TO BE IMPLEMENTED (important for guard)
    # type: ignore[override]
    def get_owner_id(self, resource_id) -> str:
        raise NotImplemented


user_service = UserService
