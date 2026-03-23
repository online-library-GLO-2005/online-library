from flask import Blueprint, request, jsonify
from services.book_service import list_books, add_book
from schemas.book_schema import BookCreateSchema, BookResponseSchema

bp = Blueprint("books", __name__, url_prefix="/books")

@bp.get("/")
def get_books():
    books = list_books()
    return BookResponseSchema(many=True).dump(books)

@bp.post("/")
def post_book():
    data = BookCreateSchema().load(request.json)
    book = add_book(data)
    return BookResponseSchema().dump(book), 201