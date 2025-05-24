from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Union

from app.config.constants import (
    ALGORITHM, SECRET_KEY
)
from app.services import users as user_service


def authenticate_user(username: str, password: str):
    try:
        user = user_service.get_user_by_email_and_password(
                email=username,
                password=password
            )
        if user:
            return user
    except Exception as e:
        print(e)
        return None


def create_access_token(
    data: dict,
    expires_delta: Union[timedelta, None] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
