from app.config.constants import (
    CREATED, OK, FORBIDDEN,
    NOT_ALLOWED, NO_EXISTENT_PRODUCT
)
from app.database.repositories.order_items import (
    OrderItems as OrderItemsRepository
)


order_items_repository = OrderItemsRepository()


class OrderItemsService:

    def __init__(self):
        self.order_items_repository = order_items_repository

    def save(self, data: dict, user: dict) -> dict:
        data["creator_id"] = user.get("id")
        data["image_url"] = "url_test"
        response = self.order_items_repository.create(data)
        return {
            "data": response,
            "message":
                "El producto fue creado"
                if response else
                "El producto no fue creado",
            "status_code": CREATED if response else OK
        }

    def get_by_id(self, id: int) -> dict:
        response = self.order_items_repository.get_by_id(id)
        if response:
            response = response.to_json()
        return {
            "data": response if response else {},
            "message":
                "El producto consultado" if response else NO_EXISTENT_PRODUCT,
            "status_code": OK
        }

    def get_all(self) -> dict:
        response = self.order_items_repository.get_all()
        response = [data_json.to_json() for data_json in response]
        return {
            "data": response,
            "message": "Todos los productos en la base de datos",
            "status_code": OK
        }

    def get_all_by_user(self, user: dict) -> dict:
        response = self.order_items_repository.get_all_by_user(
            user.get("id")
        )
        response = [data_json.to_json() for data_json in response]
        return {
            "data": response,
            "message": "Todos los productos del usuario",
            "status_code": OK
        }

    def update(self, id: int, data: dict, user: dict) -> dict:
        if data.get("creator_id") != user.get("id"):
            return {
                "data": False,
                "message": NOT_ALLOWED,
                "status_code": FORBIDDEN
            }
        response = self.order_items_repository.edit(id, data)
        return {
            "data": response,
            "message":
                "El producto fue actualizado"
                if response else
                "El producto no fue actualizado",
            "status_code": OK
        }

    def delete_by_id(self, id: int, user: dict) -> dict:
        product = self.order_items_repository.get_by_id(id)
        if not product:
            return {
                "data": False,
                "message": NO_EXISTENT_PRODUCT,
                "status_code": OK
            }
        product_json = product.to_json()
        if product_json.get("creator_id") != user.get("id"):
            return {
                "data": False,
                "message": NOT_ALLOWED,
                "status_code": FORBIDDEN
            }
        response = self.order_items_repository.delete_directly(product)
        return {
            "data": response,
            "message":
                "El producto fue eliminado"
                if response else
                "El producto no fue eliminado",
            "status_code": OK
        }
