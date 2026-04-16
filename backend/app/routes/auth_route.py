from flask import Blueprint, request, jsonify
from app.services.auth_service import auth_service
from flask_jwt_extended import jwt_required
from app.utils.apiResponse import success_response
from app.utils.guards import admin_required
from app.utils.security import is_admin_from_jwt
from app.schemas.auth_schema import *

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/login")
def login():
    data = LoginSchema().load(request.get_json())

    result = auth_service.login(email=data["email"], password=data["password"])

    return success_response(200, AuthSchema().dump(result))

@bp.post("/signup")
def signup():
    data = RegisterSchema().load(request.get_json())

    result = auth_service.register(
        name=data["name"], email=data["email"], password=data["password"]
    )

    return success_response(201, AuthSchema().dump(result))


@bp.post("/logout")
@jwt_required(refresh=True)
def logout():
    refresh_token = request.headers.get("Authorization").split()[1]

    auth_service.logout(refresh_token)

    return success_response(200, None, "Logged out")


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    refresh_token = request.headers.get("Authorization").split()[1]
    is_admin = is_admin_from_jwt()

    access_token = auth_service.refresh_token(refresh_token, is_admin=is_admin)

    return success_response(200, access_token)


@bp.post("/promote/<int:uid>")
@admin_required
def promote_to_admin(uid: int):
    auth_service.promote_to_admin(uid)
    return success_response(200, None, "User promoted to admin")
