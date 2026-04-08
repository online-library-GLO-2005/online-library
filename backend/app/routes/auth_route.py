from flask import Blueprint, request
from app.services.auth_service import auth_service
from flask_jwt_extended import jwt_required
from app.utils.apiResponse import success_response

bp = Blueprint("auth", __name__, url_prefix="/auth")


# PLACEHOLDER
@bp.post("/login")
def login():
    message = f"Endpoint post /{bp.name}/login called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.post("/signup")
def signup():
    message = f"Endpoint post /{bp.name}/signup called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.post("/logout")
def logout():
    message = f"Endpoint post /{bp.name}/logout called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.post("/refresh")
@jwt_required()
def refresh():
    message = f"Endpoint post /{bp.name}/refresh called"
    return success_response(201, None, message)
