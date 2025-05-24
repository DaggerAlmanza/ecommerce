from app.config.constants import CREATED, OK
from app.database.repositories.users import (
    User as UsersRepository
)
from app.helpers.security import Security
from app.helpers.util import GeneralHelpers


users_repository = UsersRepository()
security_helpers = Security()
general_helpers = GeneralHelpers()


def save_service(data: dict) -> dict:
    new_password = security_helpers.hash_password(
        data.get("password_hash")
    )
    general_helpers.update_user_password(data, new_password)
    response = users_repository.create(data)
    if response:
        response = response.to_json()
    return {
        "data": response,
        "message":
            "El usuario fue creado"
            if response else
            "El usuario no fue creado",
        "status_code": CREATED
    }


def update_service(id: int, data: dict) -> dict:
    response = users_repository.edit(id, data)
    return {
        "data": response,
        "message":
            "El usuario fue actualizado "
            if response else
            "El usuario no fue actualizado ",
        "status_code": OK
    }


def get_service(id: int) -> dict:
    response = users_repository.get_by_id(id)
    if response:
        response = response.to_json()
    return {
        "data": response if response else {},
        "message":
            "El usuario consultado" if response else "El usuario no existe",
        "status_code": OK
    }


def get_all_service() -> list:
    response = users_repository.get_all()
    response = [data_json.to_json() for data_json in response]
    return {
        "data": response,
        "message": "Todos los usuario en la base de datos",
        "status_code": OK
    }


def get_user_by_email_and_password(email: str, password: str) -> dict:
    password_hash = security_helpers.hash_password(password)
    response = users_repository.get_by_email(
        email
    )
    is_password_correct = security_helpers.verify_password(
        password, password_hash
    )
    if response and is_password_correct:
        return response.to_json()
    return {}


def get_user_with_email(email: str) -> dict:
    response = users_repository.get_by_email(email)
    if response:
        return response.to_json()
    return {}
