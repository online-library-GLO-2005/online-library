from flask import Blueprint, request
from app.services.book_service import book_service
from app.utils.apiResponse import success_response
from app.schemas.book_schema import BookSchema
from app.utils.guards import admin_required

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.get("/")
def get_all():
    books = book_service.get_books()
    # On utilise many=True car c'est une liste
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