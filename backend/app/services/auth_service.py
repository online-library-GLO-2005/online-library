from app.repositories.auth_repo import auth_repo


class AuthService:
    def __init__(self):
        self._repo = auth_repo


auth_service = AuthService()
