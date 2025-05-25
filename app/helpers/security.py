import bcrypt
import re


class Security:

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashea una contraseña utilizando bcrypt.
        """
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt(rounds=12)
        )
        return hashed_password.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña en texto plano coincide con un hash bcrypt dado.
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), hashed_password.encode('utf-8')
            )
        except ValueError:
            return False

    @staticmethod
    def is_hashed(password: str) -> bool:
        """
        Verifica si una contraseña está cifrada con bcrypt.
        """
        pattern = r"^\$2[abxy]\$\d{2}\$[./0-9A-Za-z]{53}$"
        return bool(re.match(pattern, password))
