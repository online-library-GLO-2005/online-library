from flask import Blueprint, request
from app.services.author_service import author_service
from app.utils.apiResponse import success_response
from app.utils.guards import admin_required
from app.schemas.author_schema import AuthorSchema

from app.utils.apiResponse import error_response
from app.schemas.book_schema import BookSchema

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


@bp.get("/<int:aid>/books")
def get_author_books(aid):
    try:
        author = author_service.get_author_by_id(aid)
        if not author:
            return error_response(404, "Auteur introuvable")
        books = author_service.get_books_by_author(aid)
        return success_response(200, BookSchema(many=True).dump(books), "Livres de l'auteur récupérés")
    except Exception as e:
        return error_response(500, str(e))