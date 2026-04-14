from flask import Blueprint, request
from app.services.author_service import author_service
from app.utils.apiResponse import success_response
from app.utils.guards import admin_required
from app.schemas.author_schema import AuthorSchema

bp = Blueprint("authors", __name__, url_prefix="/authors")

@bp.get("/")
def get_authors():
    authors = author_service.get_authors()
    return success_response(200, authors, "Succès")

@bp.get("/<int:id>")
def get_by_id(id):
    author = author_service.get_author_by_id(id)
    return success_response(200, AuthorSchema().dump(author), "Auteur trouvé")

@bp.post("/")
@admin_required
def add_author():
    data = AuthorSchema().load(request.json)
    new_author = author_service.create_author(data)
    return success_response(201, AuthorSchema().dump(new_author), "Auteur ajouté")

@bp.put("/<int:id>")
@admin_required
def update_author(id):
    data = AuthorSchema().load(request.json, partial=True)
    updated = author_service.update_author(id, data)
    return success_response(200, AuthorSchema().dump(updated), "Auteur mis à jour")

@bp.delete("/<int:id>")
@admin_required
def delete_author(id):
    author_service.delete_author(id)
    return success_response(200, None, "Auteur supprimé")