from functools import wraps
from app.errors import AppError
from app.utils.security import is_admin_from_jwt, get_user_id
from flask_jwt_extended import verify_jwt_in_request


## Put @admin_required above routes that need that permission.
# Also verifies JWT so @jwt_required is not needed
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        if not is_admin_from_jwt():
            raise AppError(403, "User is not admin")
        return f(*args, **kwargs)

    return decorated


# This guard needs the targeted service to have a method called
def require_owner_or_admin(get_owner_id_fn, resource_id_arg="id"):
    """
    service: the service to fetch the resource
    resource_id_arg: the name of the route argument containing the resource ID
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resource_id = kwargs.get(resource_id_arg)
            if resource_id is None:
                raise AppError(400, "Missing resource id")

            verify_jwt_in_request()

            if is_admin_from_jwt():
                return f(*args, **kwargs)

            resource_user_id = get_owner_id_fn(resource_id)
            if resource_user_id is None:
                raise AppError(404, "Resource not found")

            if resource_user_id != get_user_id():
                raise AppError(403, "User is not owner")

            return f(*args, **kwargs)

        return wrapper

    return decorator
