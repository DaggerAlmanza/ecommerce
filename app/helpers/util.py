from app.helpers.security import Security


security = Security()


class GeneralHelpers:

    @staticmethod
    def setter_object_attrs(obj, keys: list, data: dict) -> None:
        """
        Asigna los valores de un diccionario a los atributos de un objeto
        """
        for key in keys:
            if key in data:
                setattr(obj, key, data.get(key))

    def update_user_password(self, data: dict, password: str):
        """
        Actualiza la contraseña de un usuario
        """
        data["password_hash"] = security.hash_password(password)
