from flask import Blueprint, request
from app.services.search_service import search_service
from app.utils.apiResponse import success_response

bp = Blueprint("search", __name__, url_prefix="/search")


# PLACEHOLDER
@bp.get("/")
def search():
    message = f"Endpoint get /{bp.name} called"
    return success_response(201, None, message)
