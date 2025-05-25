from app.config.db_connection import session
from app.helpers.util import GeneralHelpers
from app.database.models import OrderItems as OrderItemsModel
from app.database.repositories.repository import Repository


class OrderItems(Repository):

    def __init__(self):
        self.session = session
        self.conn = OrderItemsModel

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
