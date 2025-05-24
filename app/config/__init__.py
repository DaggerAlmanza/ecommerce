from fastapi import Depends, FastAPI
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.config import routers
from app.config.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    UNAUTHORIZED
)
from app.controllers.serializers.authenticate import Token
from app.controllers.views.authenticate import (
    get_current_active_user,
)
from app.controllers.serializers.users import UserAuthentication
from app.services.authenticate import authenticate_user
from app.services.authenticate import create_access_token


app = FastAPI(
    title="E-commerce API",
    description="API for E-commerce",
    version="0.1",
    redoc_url="/redoc"
)


app.include_router(
    routers.urls,
)


@app.post(
    "/token",
    tags=["session"],
    response_model=Token
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user["email"]
            },
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    "/current_user",
    tags=["session"],
    response_model=UserAuthentication
)
async def read_user_me(
    current_user: UserAuthentication = Depends(get_current_active_user)
):
    return current_user
