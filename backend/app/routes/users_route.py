from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import user_service
from app.schemas.user_schema import UserSchema
from app.schemas.book_schema import BookSchema
from app.schemas.comment_schema import CommentSchema
from app.utils.apiResponse import success_response
from app.utils.guards import admin_required

bp = Blueprint("users", __name__, url_prefix="/users")

# --- PROFIL PERSO ---


@bp.get("/me")
@jwt_required()
def get_me():
    user = user_service.get_user_profile(get_jwt_identity())
    return success_response(200, UserSchema().dump(user), "Profil récupéré")


@bp.get("/me/comments")
@jwt_required()
def get_my_comments():
    comments = user_service.get_my_comments(get_jwt_identity())
    return success_response(
        200, CommentSchema(many=True).dump(comments), "Mes commentaires"
    )


# --- GESTION DES LIVRES (Favoris / Consultés) ---


@bp.get("/me/books")
@jwt_required()
def get_my_history():
    books = user_service.get_history(get_jwt_identity())
    return success_response(
        200, BookSchema(many=True).dump(books), "Historique de lecture"
    )


@bp.get("/me/favorites")
@jwt_required()
def get_my_favorites():
    books = user_service.get_favorites(get_jwt_identity())
    return success_response(200, BookSchema(many=True).dump(books), "Mes favoris")


@bp.post("/me/favorites")
@jwt_required()
def add_favorite():
    lid = request.json.get("book_id")
    user_service.toggle_favorite(get_jwt_identity(), lid, True)
    return success_response(201, None, "Livre ajouté aux favoris")


@bp.delete("/me/favorites/<int:book_id>")
@jwt_required()
def remove_favorite(book_id):
    user_service.toggle_favorite(get_jwt_identity(), book_id, False)
    return success_response(200, None, "Livre retiré des favoris")

    # --- ADMIN / USERS ---


@bp.get("/")
def get_all():
    users_with_admin = user_service.get_all_users()
    result = [
        {**UserSchema().dump(u), "is_admin": is_admin}
        for u, is_admin in users_with_admin
    ]
    return success_response(200, result)
