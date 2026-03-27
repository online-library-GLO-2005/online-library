from flask import Blueprint

bp = Blueprint("health", __name__)

@bp.route("/")
def health():
    return {"status" : "SERVER IS WORKING AAAAA"}, 200
