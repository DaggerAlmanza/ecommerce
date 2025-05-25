from app.config.db_connection import session
from app.helpers.util import GeneralHelpers
from app.database.models import Carts
from app.database.repositories.repository import Repository


class Cart(Repository):

    def __init__(self):
        self.session = session
        self.conn = Carts

    def __update(
        self,
        data: Carts,
        params: dict
    ) -> None:
        keys = [
            "user_id",
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

    def get_user_id_by_cart_id(self, id: int) -> dict:
        cart = self.get_by_id(id)
        if cart:
            cart = cart.to_json()
        return cart

    def get_card_id_by_user_id(self, user_id: int) -> int:
        cart = self.get_by_data_dictionary({"user_id": user_id})
        if cart:
            cart = cart.to_json()
        return cart if not cart else cart.get("id")
