from flask import Blueprint

bp = Blueprint("index", __name__)

@bp.route("/")
def index():
    return {
        "name": "Online Library API",
        "version": "1.0"
        # "docs": "/docs" # If we ever add a docs page with Swagger UI.
        }, 200
