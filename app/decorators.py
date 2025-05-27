from functools import wraps
from app.config.constants import (
    FORBIDDEN, NOT_ALLOWED, ADMIN_ROL,
    NOT_FOUND,
)
from app.database.repositories.carts import (
    Cart as CartRepository
)
from app.database.repositories.cart_items import (
    CartItem as CartItemsRepository
)


_cart_repository_decorator = CartRepository()
_cart_items_repository_decorator = CartItemsRepository()


def admin_forbidden(func):
    """
    Decorador para restringir el acceso al ADMIN en la vista de API.
    asincronizado
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user")
        if not user and len(args) > 1 and isinstance(args[1], dict):
            user = args[1]

        if user and user.get("role") == ADMIN_ROL:
            return {
                "data": None,
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
        user = kwargs.get("user")
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


def ensure_cart_and_items_exist(func):
    """
    Decorador que verifica la existencia del carrito de un usuario y si tiene ítems.
    """
    @wraps(func)
    def wrapper(self, user: dict, *args, **kwargs):
        user_id = user.get("id")

        cart_id = _cart_repository_decorator.get_card_id_by_user_id(user_id)
        if not cart_id:
            return {
                "data": {},
                "message": "El carrito no existe para este usuario.",
                "status_code": NOT_FOUND
            }

        cart_items = _cart_items_repository_decorator.get_all_match({"cart_id": cart_id})
        if not cart_items:
            return {
                "data": {},
                "message": "Los artículos no existen para este carrito.",
                "status_code": NOT_FOUND
            }
        return func(self, user, *args, **kwargs)
    return wrapper
