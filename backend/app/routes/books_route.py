from flask import Blueprint, request
from app.services.book_service import book_service
from flask_jwt_extended import jwt_required
from app.utils.guards import admin_required
from app.utils.apiResponse import success_response
from app.schemas.book_schema import BookSchema

# from app.services.book_service import insert_book, get_books


bp = Blueprint("books", __name__, url_prefix="/books")


# PLACEHOLDER
# Should accept queries
@bp.get("/")
def get_all():
    message = f"Endpoint get /{bp.name} called"
    return success_response(201, None, message)


# PLACEHOLDER
# Should accept queries
@bp.get("/:id")
def get_by_id():
    message = f"Endpoint get /{bp.name}/:id called"
    return success_response(201, None, message)


@bp.post("/")
@admin_required
def add_book():
    # schema = BookSchema()
    # data = schema.load(request.json)

    # Call service logic
    # dump with marshmallow
    # Replace "None" here with the marshmallow result
    message = f"Endpoint post /{bp.name} called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.put("/:id")
@admin_required
def update_book():
    message = f"Endpoint put /{bp.name}/:id called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.delete("/:id")
@admin_required
def delete_book():
    message = f"Endpoint delete /{bp.name}/:id called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.get("/:id/comments")
def get_book_comments():
    message = f"Endpoint get /{bp.name}/:id/comments called"
    return success_response(201, None, message)


# PLACEHOLDER
@bp.post("/:id/comments")
@jwt_required()
def add_book_comment():
    message = f"Endpoint post /{bp.name}/:id/comments called"
    return success_response(201, None, message)
