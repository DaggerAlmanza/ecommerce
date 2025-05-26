from app.config.db_connection import session
from app.helpers.util import GeneralHelpers
from app.database.models import Products as ProductsModel
from app.database.repositories.repository import Repository


class Products(Repository):

    def __init__(self):
        self.session = session
        self.conn = ProductsModel

    def __update(
        self,
        data: ProductsModel,
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
        data = self.find_one_not_deleted(id)
        if not data:
            return False
        self.__update(data, params)
        self.session.commit()
        self.session.close()
        return True
