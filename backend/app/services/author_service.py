from app.repositories.author_repo import author_repo


class AuthorService:
    def __init__(self):
        self._repo = author_repo


author_service = AuthorService()
