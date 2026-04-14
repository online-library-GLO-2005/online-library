from datetime import datetime
from app.repositories.auth_repo import auth_repo
from app.utils.security import *
from app.errors import AppError
from datetime import datetime, timedelta


class AuthService:
    def __init__(self):
        self._repo = auth_repo

    def login(self, email: str, password: str):
        user = self._repo.find_user_by_email(email)

        if not user:
            raise AppError(401, "Invalid email or password")

        if not comparePassword(password, user.password_hash):
            raise AppError(401, "Invalid email or password")

        is_admin = self._repo.is_admin(user.id)

        access_token = generate_access_token(str(user.id), is_admin=is_admin)
        refresh_token = generate_refresh_token(str(user.id), is_admin=is_admin)

        # extract jti from refresh token
        jti = get_jti(refresh_token)

        expires_at = datetime.utcnow() + timedelta(days=7)
        self._repo.store_refresh_token(
            uid=user.id,
            jti=jti,
            token_hash=hash_token(refresh_token),
            expires_at=expires_at,
        )

        return {
            "user": self._to_user_dict(user),
            "is_admin": is_admin,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def register(self, name: str, email: str, password: str):
        hashed_password = hashPassword(password)
        user = self._repo.find_user_by_email(
            email
        )  # check if email already exists, will raise error if it does
        if user:
            raise AppError(400, "Email already in use")

        self._repo.register(name, email, hashed_password)

        return self.login(email, password)

    def logout(self, refresh_token: str):
        jti = get_jti(refresh_token)
        self._repo.revoke_refresh_token(jti)

    def promote_to_admin(self, uid: int):
        self._repo.promote_to_admin(uid)

    def refresh_token(self, refresh_token: str, is_admin: bool = False):
        jti = get_jti(refresh_token)

        token = self._repo.get_refresh_token_by_jti(jti)

        if not token:
            raise AppError(401, "Invalid refresh token")

        if token["revoked"] == 1:
            raise AppError(401, "Token revoked")

        if token["expires_at"] < datetime.utcnow():
            raise AppError(401, "Token expired")

        # extra security
        if token["token_hash"] != hash_token(refresh_token):
            raise AppError(401, "Invalid token")

        access_token = generate_access_token(str(token["UID"]), is_admin)

        return {"access_token": access_token}

    def _to_user_dict(self, user):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "birth_date": user.birth_date,
            "phone": user.phone,
            "address": user.address,
            "created_at": user.created_at,
        }


auth_service = AuthService()
