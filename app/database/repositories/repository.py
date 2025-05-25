from app.config.db_connection import session
from app.database.models import Base


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
            print(error)
            return False

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
