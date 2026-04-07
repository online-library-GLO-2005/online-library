from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.utils.guards import admin_required
from app.utils.apiResponse import success_response
from app.schemas.book_schema import BookSchema

# from app.services.book_service import insert_book, get_books


bp = Blueprint("books", __name__, url_prefix="/books")


# Should accept queries
@bp.get("/")
def list_books():
    return success_response(201, None, "Endpoint get /books called")


# TODO: We still need params and headers validators if needed
@bp.post("/")
@jwt_required()  # Always this before admin_required
@admin_required
def add_book():
    schema = BookSchema()
    data = schema.load(request.json)

    # Call service logic
    # dump with marshmallow
    # Replace "None" here with the marshmallow result
    return success_response(201, None, "Book created")
