from app.services.ownable_service import OwnableService
from app.repositories.user_repo import user_repo
from app.errors import AppError
from app.schemas.user_schema import UserSchema


class UserService(OwnableService):
    def __init__(self):
        self._repo = user_repo

    # TODO: this is not really ownable, anyone can access any profile. We can either:
    # 1) if the requested profile is their own
    def get_owner_id(self, resource_id) -> str:
        return str(resource_id)

    def get_user_profile(self, uid: int):
        user = self._repo.get_by_id(uid)
        if not user:
            raise AppError(404, "Utilisateur introuvable")
        return user, self._repo.is_admin(uid)  # return tuple, not dict

    def update_user(self, uid: int, data: dict):
        self._repo.update(uid, data)
        return self._repo.get_by_id(uid)

    def delete_user(self, uid: int):
        self._repo.delete(uid)

    def get_history(self, uid: int):
        books_data = self._repo.get_consulted_books(uid)
        return books_data

    def get_favorites(self, uid: int):
        books_data = self._repo.get_favorite_books(uid)
        return books_data

    def toggle_favorite(self, uid: int, lid: int, is_fav: bool):
        if is_fav:
            self._repo.add_to_favorites(uid, lid)
        else:
            self._repo.remove_from_favorites(uid, lid)

    def get_my_comments(self, uid: int):
        comments_data = self._repo.get_user_comments(uid)
        return comments_data

    def get_all_users(self):
        users = self._repo.get_all_users()
        return [(u, self._repo.is_admin(u.id)) for u in users]


user_service = UserService()
