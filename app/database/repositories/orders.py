from app.config.db_connection import session
from app.database.models import Orders as OrdersModel
from app.database.repositories.cart_items import (
    CartItem as CartItemsRepository
)
from app.database.repositories.repository import Repository
from app.helpers.util import GeneralHelpers
from app.database.models import OrderItems as OrderItemsModel

cart_items_repository = CartItemsRepository()


class Orders(Repository):

    def __init__(self):
        self.session = session
        self.conn = OrdersModel
        self.order_items = OrderItemsModel

    def __update(
        self,
        data: OrdersModel,
        params: dict
    ) -> None:
        keys = [
            "status",
        ]
        GeneralHelpers.setter_object_attrs(data, keys, params)

    def edit(self, id: int, params: dict):
        data = self.get_by_id(id)
        if not data:
            return False
        self.__update(data, params)
        self.session.commit()
        self.session.close()
        return True

    def create_with_transaction(
        self, orders: dict, order_items: list, cart_items: list
    ) -> bool:
        try:
            order = self.conn(**orders)
            self.session.add(order)
            self.session.flush()
            for item in order_items:
                item.update({"order_id": order.id})
                order_item = self.order_items(**item)
                self.session.add(order_item)
                self.session.flush()
            for item in cart_items:
                self.session.delete(item)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al hacer el proceso (orden, articulo y carrito): {e}")
            return False
        finally:
            session.close()
