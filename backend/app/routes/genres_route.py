from flask import Blueprint, request
from app.services.genre_service import genre_service
from app.utils.apiResponse import success_response
from app.utils.guards import admin_required
from app.schemas.genre_schema import GenreSchema

from app.utils.apiResponse import error_response
from app.schemas.book_schema import BookSchema

bp = Blueprint("genres", __name__, url_prefix="/genres")

@bp.get("/")
def get_all():
    genres = genre_service.get_all_genres()
    return success_response(200, GenreSchema(many=True).dump(genres), "Liste des genres récupérée")

@bp.get("/<int:id>")
def get_by_id(id):
    genre = genre_service.get_genre_by_id(id)
    return success_response(200, GenreSchema().dump(genre), "Genre trouvé")

@bp.post("/")
@admin_required
def add_genre():
    data = GenreSchema().load(request.json)
    new_genre = genre_service.create_genre(data['name'])
    return success_response(201, GenreSchema().dump(new_genre), "Genre créé")

@bp.put("/<int:id>")
@admin_required
def update_genre(id):
    data = GenreSchema().load(request.json)
    updated = genre_service.update_genre(id, data['name'])
    return success_response(200, GenreSchema().dump(updated), "Genre mis à jour")

@bp.delete("/<int:id>")
@admin_required
def delete_genre(id):
    genre_service.delete_genre(id)
    return success_response(200, None, "Genre supprimé")


@bp.get("/<int:gid>/books")
def get_genre_books(gid):

    genre = genre_service.get_genre_by_id(gid)
    if not genre:
        return error_response(404, "Genre introuvable")
    books = genre_service.get_books_by_genre(gid)
    return success_response(200, BookSchema(many=True).dump(books), "Livres du genre récupérés")