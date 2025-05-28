from fastapi import UploadFile

from app.config.constants import (
    CREATED, OK, FORBIDDEN, NOT_ALLOWED,
)
from app.database.repositories.products import (
    Products as ProductsRepository
)
from app.decorators import user_forbidden
from app.helpers.util import GeneralHelpers

general_helpers = GeneralHelpers()
products_repository = ProductsRepository()
NO_EXISTENT_PRODUCT = "El producto no existe"


class ProductsService:

    def __init__(self):
        self.products_repository = products_repository
        self.general_helpers = general_helpers

    @user_forbidden
    def save(self, user: dict, data: dict) -> dict:
        data["creator_id"] = user.get("id")
        response = self.products_repository.create(data)
        return {
            "data": response,
            "message":
                "El producto fue creado"
                if response else
                "El producto no fue creado",
            "status_code": CREATED if response else OK
        }

    @user_forbidden
    def image_url(self, file: UploadFile) -> dict:
        response = self.general_helpers.upload_file(file)
        return {
            "data": response,
            "message":
                "El archivo fue subido"
                if response else
                "El archivo no fue subido",
            "status_code": CREATED if response else OK
        }

    def get_by_id(self, id: int) -> dict:
        response = self.products_repository.find_one_not_deleted(id)
        if response:
            response = response.to_json()
        return {
            "data": response if response else {},
            "message":
                "El producto consultado" if response else NO_EXISTENT_PRODUCT,
            "status_code": OK
        }

    @user_forbidden
    def get_all_deleted(self, user: dict) -> dict:
        response = self.products_repository.find_many_deleted()
        response = [data_json.to_json() for data_json in response]
        return {
            "data": response,
            "message": "Todos los productos eliminados en la base de datos",
            "status_code": OK
        }

    def get_all(self) -> dict:
        response = self.products_repository.find_many_not_deleted()
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
        product = self.products_repository.find_one_not_deleted(id)
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
        response = self.products_repository.soft_delete_directly(product)
        return {
            "data": response,
            "message":
                "El producto fue eliminado"
                if response else
                "El producto no fue eliminado",
            "status_code": OK
        }
