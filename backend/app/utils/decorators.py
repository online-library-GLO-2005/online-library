from functools import wraps
from app.utils.security import is_admin


## Put @admin_required above routes that need that permission.
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_admin():
            return  # Put error here
        return f(*args, **kwargs)

    return decorated
