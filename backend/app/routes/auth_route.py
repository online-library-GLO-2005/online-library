from flask import Blueprint, request, jsonify
from app.services.auth_service import auth_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.apiResponse import success_response
from app.utils.guards import admin_required
from app.utils.security import is_admin_from_jwt
from app.errors import AppError
from app.schemas.auth_schema import *


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/login")
def login():
    data = LoginSchema().load(request.get_json())

    result = auth_service.login(email=data["email"], password=data["password"])

    response = success_response(200, AuthSchema().dump(result))
    response.set_cookie(
        "refresh_token",
        result["refresh_token"],  # or result.refresh_token depending on type
        httponly=True,
        secure=False,  # True in prod (HTTPS)
        samesite="Lax",
        max_age=7 * 24 * 60 * 60,
        path="/",
    )
    return response

@bp.post("/signup")
def signup():
    data = RegisterSchema().load(request.get_json())

    result = auth_service.register(
        name=data["name"], email=data["email"], password=data["password"]
    )

    response = success_response(201, AuthSchema().dump(result))
    response.set_cookie(
        "refresh_token",
        result["refresh_token"],  # or result.refresh_token depending on type
        httponly=True,
        secure=False,  # True in prod (HTTPS)
        samesite="Lax",
        max_age=7 * 24 * 60 * 60,
        path="/",
    )
    return response


@bp.post("/logout")
def logout():
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise AppError(401, "Missing refresh token")

    auth_service.logout(refresh_token)

    return success_response(200, None, "Logged out")


@bp.post("/refresh")
def refresh():
    # Par cookies
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise AppError(401, "Missing refresh token")

    is_admin = is_admin_from_jwt(refresh_token)

    result = auth_service.refresh_token(refresh_token=refresh_token, is_admin=is_admin)

    return success_response(200, result)


@bp.post("/promote/<int:uid>")
@admin_required
def promote_to_admin(uid: int):
    auth_service.promote_to_admin(uid)
    return success_response(200, None, "User promoted to admin")
