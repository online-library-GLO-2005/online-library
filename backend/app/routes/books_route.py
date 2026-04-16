from flask import Blueprint, request, jsonify
from app.services.book_service import book_service
from app.utils.apiResponse import success_response
from app.schemas.book_schema import BookSchema
from app.utils.guards import admin_required

from app.schemas import comment_schema
from app.services.comment_service import comment_service
from app.schemas.author_schema import AuthorSchema
from app.schemas.genre_schema import GenreSchema
from app.schemas.comment_schema import CommentSchema

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.get("/")
def get_all():
    books = book_service.get_books()
    return success_response(200, BookSchema(many=True).dump(books), "Livres récupérés")


@bp.get("/<int:book_id>")
def get_by_id(book_id):
    book = book_service.get_book_by_id(book_id)
    return success_response(200, BookSchema().dump(book), "Livre trouvé")


@bp.post("/")
@admin_required
def add_book():
    schema = BookSchema()
    data = schema.load(request.json)

    new_book = book_service.insert_book(data)

    return success_response(201, schema.dump(new_book), "Livre créé avec succès")


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


@bp.get("/<int:id>")
def get_book_full_details(id):
    detailed_book = book_service.get_book_details(id)
    return success_response(200, detailed_book, "Détails du livre récupérés")


# Utilise la classe directement pour créer l'instance
@bp.route("/<int:lid>/comments", methods=["GET"])
def get_book_comments(lid):
    comments = comment_service.get_comments_by_book(lid)
    schema = CommentSchema(many=True)
    return jsonify(schema.dump(comments)), 200

@bp.get("/<int:lid>/authors")
def get_book_authors(lid):
    # On récupère les auteurs via le service
    authors = book_service.get_authors_by_book(lid)
    return success_response(200, AuthorSchema(many=True).dump(authors), "Auteurs du livre récupérés")

@bp.get("/<int:lid>/genres")
def get_book_genres(lid):
    # On récupère les genres via le service
    genres = book_service.get_genres_by_book(lid)
    return success_response(200, GenreSchema(many=True).dump(genres), "Genres du livre récupérés")

