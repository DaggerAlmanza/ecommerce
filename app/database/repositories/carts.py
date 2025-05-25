from app.config.db_connection import session
from app.helpers.util import GeneralHelpers
from app.database.models import Carts as CartsModel
from app.database.repositories.repository import Repository


class Cart(Repository):

    def __init__(self):
        self.session = session
        self.conn = CartsModel

    def get_user_id_by_cart_id(self, id: int) -> dict:
        cart = self.get_by_id(id)
        if cart:
            cart = cart.to_json()
        return cart

    def get_card_id_by_user_id(self, user_id: int) -> int:
        cart = self.get_first_match({"user_id": user_id})
        if cart:
            cart = cart.to_json()
        return cart if not cart else cart.get("id")
