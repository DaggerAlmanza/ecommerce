from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from typing import Annotated

from app.controllers.serializers.response import (
    Response as ResponseSerializer
)
from app.controllers.serializers.users import (
    User as userSerializer
)
from app.services import users as user_service
from app.controllers.views.authenticate import get_current_user


router = APIRouter()


@router.post(
    "/users",
    tags=["users"],
    response_model=ResponseSerializer
)
async def create_users(
    request: userSerializer,
):
    response = user_service.save_service(
        request.model_dump()
    )
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.put(
    "/users/{id}",
    tags=["users"],
    response_model=ResponseSerializer
)
async def update_users(
    request: userSerializer,
    id: str,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = user_service.update_service(
        id,
        request.model_dump()
    )
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/users/{id}",
    tags=["users"],
    response_model=ResponseSerializer
)
async def get_users(
    id: str,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = user_service.get_service(id)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/users",
    tags=["users"],
    response_model=ResponseSerializer
)
async def get_all_users(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    print(current_user)
    response = user_service.get_all_service()
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
