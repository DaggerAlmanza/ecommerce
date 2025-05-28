from app.config.db_connection import session
from app.database.models import (
    OrderItems as OrderItemsModel,
    Orders as OrdersModel
)
from app.database.repositories.repository import Repository
from app.helpers.util import GeneralHelpers


class OrderItems(Repository):

    def __init__(self):
        self.session = session
        self.conn = OrderItemsModel
        self.orders = OrdersModel

    def __update(
        self,
        data: OrderItemsModel,
        params: dict
    ) -> None:
        keys = [
            "name",
            "description",
            "price",
            "stock_quantity",
            "image_url",
            "creator_id",
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

    def get_all_by_user(self, user_id: int) -> list:
        order_items = self.session.query(self.conn).join(
            self.orders
        ).filter(self.orders.user_id == user_id).all()
        return order_items
