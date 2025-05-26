from app.config.constants import (
    CREATED, OK, FORBIDDEN, ADMIN_ROL,
    NOT_ALLOWED
)
from app.database.repositories.carts import (
    Cart as CartsRepository
)
from app.helpers.security import Security
from app.helpers.util import GeneralHelpers
from app.decorators import user_forbidden


carts_repository = CartsRepository()
security_helpers = Security()
general_helpers = GeneralHelpers()


class CartService:

    def __init__(self):
        self.carts_repository = carts_repository

    def save(self, user: dict) -> dict:
        data = {
            "user_id": user.get("id")
        }
        response = self.carts_repository.create(data)
        return {
            "data": response,
            "message":
                "El carrito de compras fue creado"
                if response else
                "El carrito de compras no fue creado",
            "status_code": CREATED if response else OK
        }

    def get_by_id(self, id: int, user: dict) -> dict:
        cart = self.carts_repository.get_by_id(id)
        if cart:
            cart = cart.to_json()
        if cart.get("user_id") == user.get("id") or user.get("role") == ADMIN_ROL:
            response = self.carts_repository.get_by_id(id)
            if response:
                response = response.to_json()
            return {
                "data": response if response else {},
                "message":
                    "El carrito de compras consultado" if response else "El carrito de compras no existe",
                "status_code": OK
            }
        return {
                "data": {},
                "message": NOT_ALLOWED,
                "status_code": FORBIDDEN
            }

    @user_forbidden
    def get_all(self, user: dict) -> dict:
        response = self.carts_repository.get_all()
        response = [data_json.to_json() for data_json in response]
        return {
            "data": response,
            "message": "Todos los carrito de compras en la base de datos",
            "status_code": OK
        }
