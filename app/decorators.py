from functools import wraps
from app.config.constants import FORBIDDEN, NOT_ALLOWED, ADMIN_ROL


def admin_forbidden(func):
    """
    Decorador para restringir el acceso al ADMIN.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("current_user")
        if not user and len(args) > 1 and isinstance(args[1], dict):
            user = args[1]

        if user and user.get("role") == ADMIN_ROL:
            return {
                "data": [],
                "message": f"{NOT_ALLOWED} eres un administrador",
                "status_code": FORBIDDEN
            }
        return func(*args, **kwargs)
    return wrapper


def user_forbidden(func):
    """
    Decorador para restringir el acceso al USER.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("current_user")
        if not user and len(args) > 1 and isinstance(args[1], dict):
            user = args[1]

        if user and user.get("role") != ADMIN_ROL:
            return {
                "data": [],
                "message": f"{NOT_ALLOWED} eres un usuario",
                "status_code": FORBIDDEN
            }
        return func(*args, **kwargs)
    return wrapper
