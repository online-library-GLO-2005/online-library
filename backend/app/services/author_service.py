from app.repositories.author_repo import author_repo
from app.errors import AppError


class AuthorService:
    def __init__(self):
        self._repo = author_repo

    def get_authors(self, search_name=None):
        return self._repo.get_all(search_name)

    def get_author_by_id(self, aid: int):
        author = self._repo.get_by_id(aid)
        if not author:
            raise AppError(404, "Auteur introuvable")
        return author

    def create_author(self, data: dict):
        return self._repo.create(data)

    def update_author(self, aid: int, data: dict):
        self.get_author_by_id(aid)  # Check existence
        self._repo.update(aid, data)
        return self._repo.get_by_id(aid)

    def delete_author(self, aid: int):
        self.get_author_by_id(aid)
        self._repo.delete(aid)

    def get_books_by_author(self, aid: int):
        return self._repo.get_books_by_author(aid)


author_service = AuthorService()
