from app.config.constants import (
    CREATED, OK, FORBIDDEN, NOT_ALLOWED,
    UNPROCESSABLE_ENTITY,
)
from app.database.repositories.cart_items import (
    CartItem as CartItemssRepository
)
from app.database.repositories.carts import Cart as CartsRepository
from app.database.repositories.products import Products as ProductRepository
from app.decorators import admin_forbidden, user_forbidden
from app.helpers.util import GeneralHelpers


cart_items_repository = CartItemssRepository()
carts_repository = CartsRepository()
general_helpers = GeneralHelpers()
product_repository = ProductRepository()

IT_IS_NOT_MINE = f"{NOT_ALLOWED}, el artículo no pertenece a ti"


class CartItemsService:

    def __init__(self):
        self.cart_items_repository = cart_items_repository
        self.general_helpers = general_helpers
        self.carts_repository = carts_repository
        self.product_repository = product_repository
        self.product = None

    def get_user_id_by_cart_id(self, id: int) -> dict:
        cart = self.carts_repository.get_user_id_by_cart_id(id)
        return cart

    def get_card_id_by_user_id(self, id: int) -> int:
        cart_id = self.carts_repository.get_card_id_by_user_id(id)
        return cart_id

    def get_product_by_id(self, product_id: int):
        product = self.product_repository.get_by_id(product_id)
        if product:
            self.product = product.to_json()

    def verify_exitence_of_product(self, quantity: int) -> bool:
        if self.product.get("stock_quantity") >= quantity:
            return True
        return False

    @admin_forbidden
    def save(self, user: dict, data: dict) -> dict:
        self.get_product_by_id(data.get("product_id"))
        if not self.verify_exitence_of_product(data.get("quantity")):
            return {
                "data": {},
                "message":
                    f"No tenemos suficiente stock en existencia para despachar {
                        data.get('quantity')
                        } tenemos {
                        self.product.get("stock_quantity")
                    }",
                "status_code": UNPROCESSABLE_ENTITY
            }
        cart_id = self.get_card_id_by_user_id(user.get("id"))
        if not cart_id:
            return {
                "data": {},
                "message": "El usuario no tiene carrito de compras",
                "status_code": UNPROCESSABLE_ENTITY
            }
        data["cart_id"] = cart_id
        data["price_at_add"] = self.general_helpers.multiply_and_convert_to_decimal(
            self.product.get("price"), data.get("quantity")
        )
        response = self.cart_items_repository.create(data)
        return {
            "data": response,
            "message":
                "El artículo ha sido agregado al carrito de compras"
                if response else
                "El artículo no ha sido agregado al carrito de compras",
            "status_code": CREATED if response else OK
        }

    @admin_forbidden
    def get_by_id(self, user: dict, id: int) -> dict:
        cart_item = self.cart_items_repository.get_by_id(id)
        if cart_item:
            cart_item = cart_item.to_json()
        else:
            return {
                "data": {},
                "message": "El artículo en el carrito de compras no existe",
                "status_code": OK
            }
        cart = self.get_user_id_by_cart_id(cart_item.get("cart_id"))
        if cart.get("user_id") == user.get("id"):
            return {
                "data": cart_item,
                "message": "El artículo en el carrito de compras consultado",
                "status_code": OK
            }
        return {
                "data": {},
                "message": NOT_ALLOWED,
                "status_code": FORBIDDEN
            }

    @admin_forbidden
    def get_all(self, user: dict) -> dict:
        cart_id = self.get_card_id_by_user_id(user.get("id"))
        response = self.cart_items_repository.get_all_match(
            {"cart_id": cart_id}
        )
        response = [data_json.to_json() for data_json in response]
        return {
            "data": response,
            "message": "Todos los artículos en el carrito de compras del usuario",
            "status_code": OK
        }

    @user_forbidden
    def get_all_by_admin(self, user: dict) -> dict:
        response = self.cart_items_repository.get_all()
        response = [data_json.to_json() for data_json in response]
        return {
            "data": response,
            "message": "Todos los artículo en el carrito de compras en la base de datos",
            "status_code": OK
        }

    @admin_forbidden
    def update(self, user: dict, id: int, data: dict) -> dict:
        if not self.cart_items_repository.get_by_id(id):
            return {
                "data": {},
                "message": "El artículo en el carrito de compras no existe",
                "status_code": OK
            }
        if self.get_user_id_by_cart_id(data.get("cart_id")).get("user_id") != user.get("id"):
            return {
                "data": False,
                "message": IT_IS_NOT_MINE,
                "status_code": FORBIDDEN
            }
        self.get_product_by_id(data.get("product_id"))
        if not self.verify_exitence_of_product(data.get("quantity")):
            return {
                "data": {},
                "message":
                    f"No tenemos suficiente stock en existencia para despachar {
                        data.get('quantity')
                        } tenemos {
                        self.product.get("stock_quantity")
                    }",
                "status_code": UNPROCESSABLE_ENTITY
            }
        data["price_at_add"] = self.general_helpers.multiply_and_convert_to_decimal(
            self.product.get("price"), data.get("quantity")
        )
        response = self.cart_items_repository.edit(id, data)
        return {
            "data": response,
            "message":
                "El artículo fue actualizado"
                if response else
                "El artículo no fue actualizado",
            "status_code": OK
        }

    @admin_forbidden
    def delete_by_id(self, user: dict, id: int) -> dict:
        cart = self.cart_items_repository.get_cart_items_and_carts_by_id(id)
        if cart.get("cart_id", {}).get("user_id") != user.get("id"):
            return {
                "data": False,
                "message": IT_IS_NOT_MINE,
                "status_code": FORBIDDEN
            }
        response = self.cart_items_repository.delete(id)
        return {
            "data": response,
            "message":
                "El artículo fue eliminado"
                if response else
                "El artículo no fue eliminado",
            "status_code": OK
        }
