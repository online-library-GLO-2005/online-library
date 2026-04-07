from flask import Blueprint, request, jsonify
from app.services.book_service import insert_book, get_books
from app.schemas.book_schema import BookSchema

bp = Blueprint("books", __name__, url_prefix="/books")


# Should accept queries
@bp.get("/books")
def list_books():
    return jsonify(get_books())


@bp.post("/books")
def add_book():
    schema = BookSchema()
    data = schema.load(request.json)

    # Call service logic
    return {"message": "Book added"}, 201
