from app.helpers.security import Security


class TestSecurity:

    def test_hash_password_returns_string(self):
        """
        Verifica que hash_password devuelve un string.
        """
        password = "mysecretpassword"
        hashed = Security.hash_password(password)
        assert isinstance(hashed, str)
        assert hashed.startswith('$2b$') or hashed.startswith('$2a$')
        assert len(hashed) > 50

    def test_hash_password_is_verifiable(self):
        """
        Verifica que una contraseña hasheada puede ser verificada correctamente.
        """
        password = "anothersecretpassword"
        hashed = Security.hash_password(password)
        assert Security.verify_password(password, hashed)

    def test_verify_password_correct(self):
        """
        Verifica que verify_password devuelve True para una contraseña correcta.
        """
        password = "testpassword123"
        hashed = Security.hash_password(password)
        assert Security.verify_password(password, hashed)

    def test_verify_password_incorrect(self):
        """
        Verifica que verify_password devuelve False para una contraseña incorrecta.
        """
        password = "testpassword123"
        hashed = Security.hash_password(password)
        assert Security.verify_password("wrongpassword", hashed) is False

    def test_verify_password_invalid_hash(self):
        """
        Verifica que verify_password devuelve False para un hash inválido.
        """
        plain_password = "somepassword"
        invalid_hash = "not_a_valid_bcrypt_hash"
        assert Security.verify_password(plain_password, invalid_hash) is False

    def test_verify_password_empty_password(self):
        """
        Verifica el comportamiento con una contraseña vacía.
        """
        password = ""
        hashed = Security.hash_password(password)
        assert Security.verify_password("", hashed) is True
        assert Security.verify_password(" ", hashed) is False

    def test_is_hashed_con_cadena_vacia(self):
        """
        Verifica que is_hashed devuelve False para una cadena vacía.
        """
        assert Security.is_hashed("") is False
