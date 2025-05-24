from unittest.mock import patch

from app.helpers.util import GeneralHelpers


class TestGeneralHelpers:

    def test_setter_object_attrs_basic(self):
        """
        Verifica que los atributos se asignan correctamente cuando las claves existen en los datos.
        """
        class TestObject:
            pass

        obj = TestObject()
        keys = ["name", "age"]
        data = {"name": "Alice", "age": 30, "city": "New York"}

        GeneralHelpers.setter_object_attrs(obj, keys, data)

        assert hasattr(obj, "name")
        assert obj.name == "Alice"
        assert hasattr(obj, "age")
        assert obj.age == 30
        assert not hasattr(obj, "city")

    def test_setter_object_attrs_empty_keys(self):
        """
        Verifica que no se asigna nada cuando la lista de claves está vacía.
        """
        class TestObject:
            pass

        obj = TestObject()
        keys = []
        data = {"name": "Alice"}

        GeneralHelpers.setter_object_attrs(obj, keys, data)

        assert not hasattr(obj, "name")

    def test_setter_object_attrs_data_not_in_keys(self):
        """
        Verifica que no se asigna un atributo si la clave está en 'keys' pero no en 'data'.
        """
        class TestObject:
            pass

        obj = TestObject()
        keys = ["name", "address"]
        data = {"name": "Bob"}

        GeneralHelpers.setter_object_attrs(obj, keys, data)

        assert hasattr(obj, "name")
        assert obj.name == "Bob"
        assert not hasattr(obj, "address")

    def test_setter_object_attrs_different_types(self):
        """
        Verifica que se pueden asignar diferentes tipos de datos.
        """
        class TestObject:
            pass

        obj = TestObject()
        keys = ["is_active", "value"]
        data = {"is_active": True, "value": 123.45}

        GeneralHelpers.setter_object_attrs(obj, keys, data)

        assert obj.is_active is True
        assert obj.value == 123.45

    def test_setter_object_attrs_empty_data(self):
        """
        Verifica que no se asigna nada si el diccionario de datos está vacío.
        """
        class TestObject:
            pass

        obj = TestObject()
        keys = ["name", "age"]
        data = {}

        GeneralHelpers.setter_object_attrs(obj, keys, data)

        assert not hasattr(obj, "name")
        assert not hasattr(obj, "age")

    @patch('app.helpers.util.security')
    def test_update_user_password(self, mock_security_instance):
        """
        Verifica que la contraseña se actualiza correctamente y que hash_password es llamado.
        """
        mock_security_instance.hash_password.return_value = "mocked_hashed_password_123"

        helper = GeneralHelpers()
        user_data = {"username": "testuser", "password_hash": "old_hash"}
        new_password = "new_secure_password"

        helper.update_user_password(user_data, new_password)

        mock_security_instance.hash_password.assert_called_once_with(new_password)

        assert user_data["password_hash"] == "mocked_hashed_password_123"
        assert user_data["username"] == "testuser"

    @patch('app.helpers.util.security')
    def test_update_user_password_empty_data(self, mock_security_instance):
        """
        Verifica que funciona con un diccionario de datos vacío (añadiendo la clave).
        """
        mock_security_instance.hash_password.return_value = "another_mocked_hash"

        helper = GeneralHelpers()
        user_data = {}
        new_password = "another_password"

        helper.update_user_password(user_data, new_password)

        mock_security_instance.hash_password.assert_called_once_with(new_password)
        assert user_data["password_hash"] == "another_mocked_hash"

    @patch('app.helpers.util.security')
    def test_update_user_password_none_password(self, mock_security_instance):
        """
        Verifica el comportamiento cuando la contraseña es None.
        """
        mock_security_instance.hash_password.return_value = "hashed_none"

        helper = GeneralHelpers()
        user_data = {"username": "testuser"}
        new_password = None

        helper.update_user_password(user_data, new_password)

        mock_security_instance.hash_password.assert_called_once_with(None)
        assert user_data["password_hash"] == "hashed_none"
