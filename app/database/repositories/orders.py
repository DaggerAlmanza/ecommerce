from app.config.db_connection import session
from app.helpers.util import GeneralHelpers
from app.database.models import Orders as OrdersModel
from app.database.repositories.repository import Repository
from app.database.repositories.order_items import (
    OrderItems as OrderItemsRepository
)
from app.database.repositories.cart_items import (
    CartItem as CartItemsRepository
)
from app.database.repositories.carts import (
    Cart as CartsRepository
)


cart_items = CartItemsRepository()
carts = CartsRepository()
order_items = OrderItemsRepository()


class Orders(Repository):

    def __init__(self):
        self.session = session
        self.conn = OrdersModel
        self.order_items = order_items
        self.cart_items = cart_items
        self.cart = carts
    
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

    def create_with_transaction(self, data: dict) -> bool:
        try:
            with self.session.begin():

        
        except Exception as e:
            print(f"Error al hacer el proceso (orden, articulo y carrito): {e}")
            return False
