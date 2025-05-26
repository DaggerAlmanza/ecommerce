from app.config.db_connection import session
from app.helpers.util import GeneralHelpers
from app.database.models import Users as UsersModel
from app.database.repositories.repository import Repository


class User(Repository):

    def __init__(self):
        self.session = session
        self.conn = UsersModel

    def __update(
        self,
        data: UsersModel,
        params: dict
    ) -> None:
        keys = [
            "username",
            "password_hash",
            "email",
            "adress"
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

    def get_by_email(self, email: str) -> dict:
        kwargs = {
            "deleted_at": None,
            "email": email
        }
        data = self.session.query(self.conn).filter_by(**kwargs).first()
        return data
