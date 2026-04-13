from flask import Blueprint, request
from app.services.publisher_service import publisher_service
from app.utils.apiResponse import success_response
from app.utils.guards import admin_required
from app.schemas.publisher_schema import PublisherSchema

bp = Blueprint("publishers", __name__, url_prefix="/publishers")

@bp.get("/")
def get_all():
    publishers = publisher_service.get_all_publishers()
    return success_response(200, PublisherSchema(many=True).dump(publishers), "Éditeurs récupérés")

@bp.get("/<int:id>")
def get_by_id(id):
    publisher = publisher_service.get_publisher_by_id(id)
    return success_response(200, PublisherSchema().dump(publisher), "Éditeur trouvé")

@bp.post("/")
@admin_required
def add_publisher():
    data = PublisherSchema().load(request.json)
    new_pub = publisher_service.create_publisher(data)
    return success_response(201, PublisherSchema().dump(new_pub), "Éditeur créé")

@bp.put("/<int:id>")
@admin_required
def update_publisher(id):
    data = PublisherSchema().load(request.json)
    updated = publisher_service.update_publisher(id, data)
    return success_response(200, PublisherSchema().dump(updated), "Éditeur mis à jour")

@bp.delete("/<int:id>")
@admin_required
def delete_publisher(id):
    publisher_service.delete_publisher(id)
    return success_response(200, None, "Éditeur supprimé")