from flask import Blueprint, request, jsonify
from app.services.book_service import book_service
from app.utils.apiResponse import (
    success_response,
    error_response,
)  # Ajout de error_response
from app.schemas.book_schema import BookSchema
from app.utils.guards import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.comment_service import comment_service
from app.schemas.author_schema import AuthorSchema
from app.schemas.genre_schema import GenreSchema
from app.schemas.comment_schema import CommentSchema

from app.services.rating_servie import rating_service

bp = Blueprint("books", __name__, url_prefix="/books")


# --- Routes existantes ---


@bp.get("/")
def get_all():
    books = book_service.get_books()
    return success_response(200, BookSchema(many=True).dump(books), "Livres récupérés")


@bp.get("/<int:id>")
def get_by_id(id):  # Correction ici : le paramètre doit matcher <int:id>
    detailed_book = book_service.get_book_details(id)
    return success_response(200, detailed_book, "Détails du livre récupérés")


@bp.post("/")
@admin_required
def add_book():
    schema = BookSchema()
    data = schema.load(request.json)
    new_book = book_service.insert_book(data)
    return success_response(201, schema.dump(new_book), "Livre créé avec succès")


@bp.delete("/<int:id>")
@admin_required
def delete_book(id):
    new_book = book_service.delete(id)
    return success_response(200, None, "Livre a été supprimé")


# --- Nouvelles routes de liaisons ---


@bp.post("/<int:lid>/authors/<int:aid>")
@admin_required
def link_author_to_book(lid, aid):
    book_service.link_author(lid, aid)
    return success_response(201, None, "Auteur lié au livre")


@bp.post("/<int:lid>/genres/<int:gid>")
@admin_required
def link_genre_to_book(lid, gid):
    book_service.link_genre(lid, gid)
    return success_response(201, None, "Genre lié au livre")


# --- GESTION DES COMMENTAIRES ---


@bp.route("/<int:lid>/comments", methods=["GET"])
def get_book_comments(lid):
    comments = comment_service.get_comments_by_book(lid)
    schema = CommentSchema(many=True)
    return success_response(200, schema.dump(comments), "Commentaires récupérés")


@bp.post("/<int:lid>/comments")
@jwt_required()
def add_comment(lid):

    current_user_id = get_jwt_identity()

    data = request.get_json()
    if not data or "message" not in data:
        return error_response(400, "Le message est requis")

    new_comment = comment_service.add_comment(
        user_id=current_user_id, book_id=lid, message=data["message"]
    )

    return success_response(
        201, CommentSchema().dump(new_comment), "Commentaire ajouté"
    )


# --- Récupération des relations ---


@bp.get("/<int:lid>/authors")
def get_book_authors(lid):
    authors = book_service.get_authors_by_book(lid)
    return success_response(
        200, AuthorSchema(many=True).dump(authors), "Auteurs récupérés"
    )


@bp.get("/<int:lid>/genres")
def get_book_genres(lid):
    genres = book_service.get_genres_by_book(lid)
    return success_response(
        200, GenreSchema(many=True).dump(genres), "Genres récupérés"
    )


@bp.post("/<int:lid>/ratings")
@jwt_required()
def add_rating(lid):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data or "note" not in data:
            return error_response(400, "La note est manquante")

        note = float(data["note"])

        rating_service.rate_book(current_user_id, lid, note)

        return success_response(201, {"note": note}, "Note enregistrée avec succès")

    except ValueError:
        return error_response(400, "La note doit être un nombre valide")
