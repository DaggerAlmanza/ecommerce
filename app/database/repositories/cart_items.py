from app.config.db_connection import session
from app.helpers.util import GeneralHelpers
from app.database.models import CartItems as CartItemsModel
from app.database.repositories.repository import Repository


class CartItem(Repository):

    def __init__(self):
        self.session = session
        self.conn = CartItemsModel

    def __update(
        self,
        data: CartItemsModel,
        params: dict
    ) -> None:
        keys = [
            "product_id",
            "quantity",
            "price_at_add"
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

    def get_cart_items_and_carts_by_id(self, id: int) -> dict:
        data = self.session.query(self.conn).filter_by(id=id).first()
        if data:
            data = data.to_dict()
        return data
