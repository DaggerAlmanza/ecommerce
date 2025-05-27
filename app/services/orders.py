from decimal import Decimal
from typing import Dict, Any

from app.config.constants import (
    CREATED,
    OK,
    INTERNAL_SERVER_ERROR,
    UNPROCESSABLE_ENTITY,
    ACCEPTED,
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
from app.tasks.order import process_order
from app.database.repositories.products import Products as ProductsRepository


cart_items_repository = CartItemsRepository()
cart_repository = CartRepository()
orders_repository = OrdersRepository()
products_repository = ProductsRepository()
NO_EXISTENT_PRODUCT = "La orden no existe"


class OrdersService:

    def __init__(self):
        self.orders_repository = orders_repository
        self.cart = cart_repository
        self.cart_items = cart_items_repository
        self.products = products_repository

    @admin_forbidden
    @ensure_cart_and_items_exist
    def save_async(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método para encolar la creación asíncrona de órdenes
        """
        try:
            task = process_order.delay(user)
            return {
                "task_id": task.id,
                "message": "La orden ha sido encolada para procesamiento",
                "status_code": ACCEPTED
            }
        except Exception as e:
            print(f"Error al encolar la orden: {e}")
            return {
                "message": "Error al encolar la orden",
                "status_code": INTERNAL_SERVER_ERROR
            }

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Obtener el estado de una tarea específica
        """
        try:
            from app.config.celery import celery_app
            task = celery_app.AsyncResult(task_id)
            if task.state == "PENDING":
                response = {
                    "state": task.state,
                    "message": "La tarea está pendiente de procesamiento",
                    "status_code": OK
                }
            elif task.state == "PROCESSING":
                response = {
                    "state": task.state,
                    "message": task.info.get("message", "Procesando..."),
                    "user_id": task.info.get("user_id"),
                    "status_code": OK
                }
            elif task.state == "SUCCESS":
                response = {
                    "state": task.state,
                    "result": task.result,
                    "message": "Orden procesada exitosamente",
                    "status_code": OK
                }
            else:
                print(f"Error al encolar la orden: {task.info}")
                response = {
                    "state": task.state,
                    "message": "Error procesando la orden",
                    "status_code": OK
                }
            return response
        except Exception as e:
            return {
                "state": "ERROR",
                "error": str(e),
                "message": "Error consultando el estado de la tarea",
                "status_code": INTERNAL_SERVER_ERROR
            }

    def _process_order_creation(self, user: Dict[str, Any]) -> Dict[str, Any]:
        print("Procesando la orden")
        cart_id = self.cart.get_card_id_by_user_id(
            user.get("id")
        )
        cart_items = self.cart_items.get_all_match(
            {"cart_id": cart_id}
        )
        product_quantities = {str(item.product_id): item.quantity for item in cart_items}
        for id, quantity in product_quantities.items():
            product = self.products.get_by_id(id)
            if not product.stock_quantity >= quantity:
                return {
                    "data": {},
                    "message":
                        f"No tenemos suficiente stock en existencia para despachar {
                            quantity
                            } tenemos {
                            product.stock_quantity
                        }",
                    "status_code": UNPROCESSABLE_ENTITY
                }
            else:
                product.stock_quantity -= quantity
        if cart_items:
            cart_items_to_json = [
                data_json.to_json() for data_json in cart_items
            ]
            order_items = []
            total_amount = Decimal(0)
            for item in cart_items_to_json:
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
                "total_amount": total_amount,
                "status": "PENDING"
            }
            response = self.orders_repository.create_with_transaction(
                orders, order_items, cart_items
            )
            return {
                "data": response,
                "message":
                    "La orden fue creado"
                    if response else
                    "La orden no fue creado",
                "status_code": CREATED if response else OK
            }
        return {
            "data": None,
            "message": "No hay items en el carrito",
            "status_code": OK
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
