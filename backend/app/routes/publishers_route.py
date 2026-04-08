from flask import Blueprint, request
from app.services.publisher_service import publisher_service
from app.utils.apiResponse import success_response
from app.utils.guards import admin_required

bp = Blueprint("publishers", __name__, url_prefix="/publishers")


# PLACEHOLDER - Don't forget to put queries params
@bp.get("/")
def get_all():
    message = f"Endpoint get /{bp.name} called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.get("/:id")
def get_by_id():
    message = f"Endpoint get /{bp.name}/:id called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.post("/")
@admin_required
def add_author():
    message = f"Endpoint post /{bp.name} called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.put("/:id")
@admin_required
def update_author():
    message = f"Endpoint put /{bp.name}/:id called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.delete("/:id")
@admin_required
def delete_author():
    message = f"Endpoint delete /{bp.name}/:id called"
    return success_response(201, None, message)
