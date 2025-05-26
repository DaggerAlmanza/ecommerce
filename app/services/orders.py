from app.config.constants import (
    CREATED, OK, FORBIDDEN, NOT_ALLOWED
)
from app.database.repositories.orders import (
    Orders as OrdersRepository
)
from app.database.repositories.carts import (
    Cart as CartRepository
)
from app.database.repositories.cart_items import (
    CartItem as CartItemsRepository
)
from app.decorators import (
    ensure_cart_and_items_exist,
    admin_forbidden,
    user_forbidden,
)
from decimal import Decimal

cart_items_repository = CartItemsRepository()
cart_repository = CartRepository()
orders_repository = OrdersRepository()
NO_EXISTENT_PRODUCT = "La orden no existe"


class OrdersService:

    def __init__(self):
        self.orders_repository = orders_repository
        self.cart = cart_repository
        self.cart_items = cart_items_repository

    @admin_forbidden
    @ensure_cart_and_items_exist
    def save(self, user: dict) -> dict:
        cart_id = self.cart.get_card_id_by_user_id(
            user.get("id")
        )
        cart_items = self.cart_items.get_all_match(
            {"cart_id": cart_id}
        )
        if cart_items:
            cart_items = [data_json.to_json() for data_json in cart_items]
        order_items = []
        total_amount = Decimal(0)
        for item in cart_items:
            total_amount += Decimal(item["price_at_add"])
            order_items.append(
                {
                    "product_id": item["product_id"],
                    "quantity": item["quantity"],
                    "price_at_purchase": item["price_at_add"]
                }
            )

        orders = {
            "user_id": user.get("id"),
            "total_Amount": total_amount,
            "status": "PENDING"
        }
        response = self.orders_repository.create_with_transaction(
            user, orders, order_items
        )
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

    @user_forbidden
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
