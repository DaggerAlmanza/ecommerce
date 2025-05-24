from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Annotated

from app.config.constants import (
    ALGORITHM, UNAUTHORIZED, BAD_REQUEST, SECRET_KEY
)
from app.controllers.serializers.authenticate import TokenData, MetaSerializer
from app.controllers.serializers.users import UserAuthentication
from app.services import users as user_service


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/token", tags=["session"])
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@router.get("/", tags=["meta"], response_model=MetaSerializer)
async def root():
    return {"message": "Servicio de ecommerce"}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = user_service.get_user_with_email(
        email=token_data.email
    )
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserAuthentication = Depends(get_current_user)
):
    if not current_user.get("email"):
        raise HTTPException(
            status_code=BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
