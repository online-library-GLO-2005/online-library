from flask import Blueprint, request
from app.services.comment_service import comment_service
from app.utils.apiResponse import success_response
from app.utils.guards import require_owner_or_admin

bp = Blueprint("comments", __name__, url_prefix="/comments")


# PLACEHOLDER
@bp.put("/:id")
@require_owner_or_admin(comment_service.get_owner_id)
def update_comment():
    message = f"Endpoint update /{bp.name}/:id called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.delete("/:id")
@require_owner_or_admin(comment_service.get_owner_id)
def delete_comment():
    message = f"Endpoint delete /{bp.name}/:id called"
    return success_response(201, None, message)
