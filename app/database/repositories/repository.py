# from sqlalchemy import not_

from app.config.db_connection import session
from app.database.models import Base
from app.helpers.util import GeneralHelpers


class Repository():

    def __init__(self):
        self.session = session
        self.conn = Base

    def create(self, data: dict) -> bool:
        try:
            see = self.conn(**data)
            self.session.add(see)
            self.session.commit()
            self.session.close()
            return True
        except Exception as error:
            self.session.rollback()
            print(f"Error al crear el registro: {error}")
            return False
        finally:
            self.session.close()

    def delete_directly(self, data: object):
        try:
            self.session.delete(data)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar el registro: {e}")
            return False
        finally:
            self.session.close()

    def delete(self, id: int):
        try:
            data = self.get_by_id(id)
            if not data:
                return False
            self.session.delete(data)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar el registro: {e}")
            return False
        finally:
            self.session.close()

    def get_all(self):
        data = self.session.query(self.conn).all()
        return data

    def get_by_id(self, id: int):
        data = self.session.query(self.conn).filter_by(id=id).first()
        return data

    def get_first_match(self, data: dict):
        data = self.session.query(self.conn).filter_by(**data).first()
        return data

    def get_all_match(self, data: dict):
        data = self.session.query(self.conn).filter_by(**data).all()
        return data

    def find_one_not_deleted(self, id: int):
        kwargs = {
            "deleted_at": None,
            "id": id
        }
        data = self.session.query(self.conn).filter_by(**kwargs).first()
        return data

    def find_many_not_deleted(self) -> list:
        kwargs = {
            "deleted_at": None
        }
        data = self.session.query(self.conn).filter_by(**kwargs).all()
        return data

    def find_one_deleted_by_id(self, id: int) -> dict:
        data = self.session.query(self.conn).filter_by(
            id=id
        ).filter(self.conn.deleted_at.is_not(None)).first()
        return data

    def find_many_deleted(self) -> list:
        data = self.session.query(self.conn).filter(
            self.conn.deleted_at.is_not(None)
        ).all()
        return data

    def soft_delete(self, id: int) -> bool:
        try:
            data = self.get_by_id(id)
            if not data:
                return False
            data.deleted_at = GeneralHelpers.get_datetime()
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar el registro: {e}")
            return False
        finally:
            self.session.close()

    def soft_delete_directly(self, data: object):
        try:
            data.deleted_at = GeneralHelpers.get_datetime()
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar el registro: {e}")
            return False
        finally:
            self.session.close()
