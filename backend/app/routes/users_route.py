from flask import Blueprint, request
from app.services.user_service import user_service
from flask_jwt_extended import jwt_required
from app.utils.apiResponse import success_response
from app.utils.guards import require_owner_or_admin

bp = Blueprint("users", __name__, url_prefix="/users")


# PLACEHOLDER - allows queries
@bp.get("/")
def get_all():
    message = f"Endpoint get /{bp.name} called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.get("/:id")
def get_by_id():
    message = f"Endpoint get /{bp.name}/:id called"
    return success_response(201, None, message)


# PLACEHOLDER - gets user(me) with token
@bp.get("/me")
@jwt_required()
def get_me():
    message = f"Endpoint get /{bp.name}/me called"
    return success_response(201, None, message)


# PLACEHOLDER - gets user(me) comments
@bp.get("/me/comments")
@jwt_required()
def get_comments():
    message = f"Endpoint get /{bp.name}/me/comments called"
    return success_response(201, None, message)


# PLACEHOLDER - gets user(me) saved books
@bp.get("/me/books")
@jwt_required()
def get_books():
    message = f"Endpoint get /{bp.name}/me/books called"
    return success_response(201, None, message)


# PLACEHOLDER - post user(me) saved books
@bp.post("/me/books")
@jwt_required()
def add_book():
    message = f"Endpoint post /{bp.name}/me/books called"
    return success_response(201, None, message)


# PLACEHOLDER - delete user(me) saved books
@bp.delete("/me/books/:id")
@jwt_required()
def delete_book():
    message = f"Endpoint delete /{bp.name}/me/books/:id called"
    return success_response(201, None, message)


# PLACEHOLDER - update user(me) if owner, and admin can update anyone
@bp.put("/:id")
@require_owner_or_admin(user_service.get_owner_id)
def update_user():
    message = f"Endpoint put /{bp.name}/:id called"
    return success_response(201, None, message)


# PLACEHOLDER - update user(me) if owner, and admin can update anyone
@bp.delete("/:id")
@require_owner_or_admin(user_service.get_owner_id)
def delete_user():
    message = f"Endpoint delete /{bp.name}/:id called"
    return success_response(201, None, message)
