from app.config.constants import (
    CREATED, OK, FORBIDDEN, NOT_ALLOWED,
)
from app.database.repositories.products import (
    Products as ProductsRepository
)
from app.decorators import user_forbidden


products_repository = ProductsRepository()
NO_EXISTENT_PRODUCT = "El producto no existe"


class ProductsService:

    def __init__(self):
        self.products_repository = products_repository

    @user_forbidden
    def save(self, user: dict, data: dict) -> dict:
        data["creator_id"] = user.get("id")
        data["image_url"] = "url_test"
        response = self.products_repository.create(data)
        return {
            "data": response,
            "message":
                "El producto fue creado"
                if response else
                "El producto no fue creado",
            "status_code": CREATED if response else OK
        }

    def get_by_id(self, id: int) -> dict:
        response = self.products_repository.get_by_id(id)
        if response:
            response = response.to_json()
        return {
            "data": response if response else {},
            "message":
                "El producto consultado" if response else NO_EXISTENT_PRODUCT,
            "status_code": OK
        }

    def get_all(self) -> dict:
        response = self.products_repository.get_all()
        response = [data_json.to_json() for data_json in response]
        return {
            "data": response,
            "message": "Todos los productos en la base de datos",
            "status_code": OK
        }

    @user_forbidden
    def update(self, user: dict, id: int, data: dict) -> dict:
        if data.get("creator_id") != user.get("id"):
            return {
                "data": False,
                "message": NOT_ALLOWED,
                "status_code": FORBIDDEN
            }
        response = self.products_repository.edit(id, data)
        return {
            "data": response,
            "message":
                "El producto fue actualizado"
                if response else
                "El producto no fue actualizado",
            "status_code": OK
        }

    @user_forbidden
    def delete_by_id(self, user: dict, id: int) -> dict:
        product = self.products_repository.get_by_id(id)
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
        response = self.products_repository.delete_directly(product)
        return {
            "data": response,
            "message":
                "El producto fue eliminado"
                if response else
                "El producto no fue eliminado",
            "status_code": OK
        }
