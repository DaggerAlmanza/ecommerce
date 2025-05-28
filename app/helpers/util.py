import os
from datetime import datetime
from decimal import Decimal
from fastapi import UploadFile
from pathlib import Path

from app.config.constants import ALLOWED_EXTENSIONS
from app.helpers.security import Security


security = Security()


class GeneralHelpers:

    def _generate_filename(self, extension: str):
        """Genera un nombre de archivo con la fecha y hora actual"""
        now = self.get_datetime()
        return f"image{now.strftime('%Y%m%d%H%M%S')}{extension}"

    @staticmethod
    def _validate_extension(filename: str):
        """Valida si la extensión del archivo es permitida"""
        extension = Path(filename).suffix.lower()
        return extension in ALLOWED_EXTENSIONS

    @staticmethod
    def _get_current_working_directory():
        return f"{str(os.getcwd())}"

    @staticmethod
    def _create_image_folder():
        """Crea la carpeta 'imagen' si no existe"""
        folder_path = os.path.join(os.getcwd(), 'image')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

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

    @staticmethod
    def multiply_and_convert_to_decimal(
        number_float: float, number_int: int
    ) -> Decimal:
        result = round(float(float(number_float) * number_int), 2)
        return Decimal(str(result))

    @staticmethod
    def get_datetime():
        return datetime.now()

    @staticmethod
    def send_email(
        email: str = "notificaciones@impera.com"
    ):
        print("----------------------------------")
        print(
            f"La compra se ha realizado con éxito.\
            Notificación enviada al correo a {email}"
        )
        print("----------------------------------")

    def upload_file(self, file: UploadFile) -> str:
        try:
            filename = file.filename
            if not self._validate_extension(filename):
                return ""

            filename = self._generate_filename(
                Path(file.filename).suffix.lower()
            )
            self._create_image_folder()
            path = f"{self._get_current_working_directory()}/image/{filename}"
            with open(f"image/{filename}", "wb") as image:
                image.write(file.file.read())
            return path
        except Exception as e:
            print(f"Error al guardar la imagen {e}")
            return ""
