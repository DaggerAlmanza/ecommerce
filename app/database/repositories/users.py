from app.config.db_connection import session
from app.helpers.util import GeneralHelpers
from app.database.models import Users
from app.database.repositories.repository import Repository


class User(Repository):

    def __init__(self):
        self.session = session
        self.conn = Users

    def __update(
        self,
        data: Users,
        params: dict
    ) -> None:
        keys = [
            "username",
            "password_hash",
            "email",
            "role",
            "adress"
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

    def get_by_email(self, email: str) -> dict:
        data = self.session.query(self.conn).filter_by(email=email).first()
        return data
