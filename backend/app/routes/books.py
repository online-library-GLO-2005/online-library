from flask import Blueprint, request, jsonify
from services.book_service import insert_book, get_books
from schemas.book_schema import BookCreateSchema, BookResponseSchema

bp = Blueprint("books", __name__, url_prefix="/books")

@bp.get("/")
def list_books():
    return jsonify(get_books())

@bp.post("/")
def add_book():
    schema = BookCreateSchema()
    data = schema.load(request.json)

    insert_book(data["title"], data.get("author_id"))
    return {"message": "Book added"}, 201