from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
)
import bcrypt


# === JWT for protected routes ===


# Generate a refresh token for user, longer-lived
def generate_refresh_token(user_id: str, is_admin: bool = False) -> str:
    return create_refresh_token(
        identity=user_id, additional_claims={"is_admin": is_admin}
    )


# Generate a short-lived access token (e.g., 15 min)
def generate_access_token(user_id: str, is_admin: bool = False) -> str:
    return create_access_token(
        identity=user_id, additional_claims={"is_admin": is_admin}
    )


# Get user id from jwt token, the token is passed through the decorator of the route @jwt_required()
def get_user_id() -> str:
    return get_jwt_identity()


# Verify if admin from jwt token, the token is passed through the decorator of the route @jwt_required()
def is_admin() -> bool:
    jwt_data = get_jwt()
    return bool(jwt_data.get("is_admin", False))


# === Bcrypt for password protection ===


# Bcrypt for password hashing and comparing
# Bcrypt works with bytes, so we need to encode and decode
def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def comparePassword(password: str, hashedPassword: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashedPassword.encode("utf-8"))
