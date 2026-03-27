from functools import wraps
from flask_jwt_extended import get_jwt_identity

# TODO: Make User

# from models.user import User

# def admin_required(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         user_id = get_jwt_identity()
#         user = User.query.get(user_id)
#         if not user or user.role != "admin":
#             return {"error": "Forbidden", "message": "Admin only"}, 403
#         return fn(*args, **kwargs)
#     return wrapper