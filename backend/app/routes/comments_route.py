from flask import Blueprint, request
from app.services.comment_service import comment_service
from app.utils.apiResponse import success_response
from app.utils.guards import require_owner_or_admin
from app.schemas.comment_schema import CommentSchema

bp = Blueprint("comments", __name__, url_prefix="/comments")

@bp.put("/<int:id>")
@require_owner_or_admin(comment_service.get_owner_id)
def update_comment(id):
    data = request.json
    updated_comment = comment_service.update_comment(id, data.get('message'))
    return success_response(200, CommentSchema().dump(updated_comment), "Commentaire mis à jour")

@bp.delete("/<int:id>")
@require_owner_or_admin(comment_service.get_owner_id)
def delete_comment(id):
    comment_service.delete_comment(id)
    return success_response(200, None, "Commentaire supprimé")