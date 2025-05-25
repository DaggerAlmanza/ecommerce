from app.config.constants import (
    CREATED, OK, FORBIDDEN, NOT_ALLOWED
)
from app.database.repositories.orders import (
    Orders as OrdersRepository
)


orders_repository = OrdersRepository()
NO_EXISTENT_PRODUCT = "La orden no existe"


class OrdersService:

    def __init__(self):
        self.orders_repository = orders_repository

    def save(self, id_cart: int, user: dict) -> dict:
        """
        consultar todos los items del carrito por id_cart
        crear orden
        crear cada items de la orden
        eliminar los items del carrito
        """
        data = {
            "cart_id": id_cart,
            "status": "PENDING"
        }
        cart = self.orders_repository.get_cart_by_id(id_cart)
        if not cart:
            return {
                "data": {},
                "message": NO_EXISTENT_PRODUCT,
                "status_code": FORBIDDEN
            }
        if cart.user_id != user.get("id"):
            return {
                "data": {},
                "message": NOT_ALLOWED,
                "status_code": FORBIDDEN
            }
        
        data["creator_id"] = user.get("id")
        data["image_url"] = "url_test"
        response = self.orders_repository.create(data)
        return {
            "data": response,
            "message":
                "La orden fue creado"
                if response else
                "La orden no fue creado",
            "status_code": CREATED if response else OK
        }

    def get_by_id(self, id: int) -> dict:
        response = self.orders_repository.get_by_id(id)
        if response:
            response = response.to_json()
        return {
            "data": response if response else {},
            "message":
                "La orden consultada" if response else NO_EXISTENT_PRODUCT,
            "status_code": OK
        }

    def get_all(self) -> dict:
        response = self.orders_repository.get_all()
        response = [data_json.to_json() for data_json in response]
        return {
            "data": response,
            "message": "Todas las ordenes en la base de datos",
            "status_code": OK
        }

    def update(self, id: int, data: dict) -> dict:
        response = self.orders_repository.edit(id, data)
        return {
            "data": response,
            "message":
                "La orden fue actualizado"
                if response else
                "La orden no fue actualizado",
            "status_code": OK
        }
