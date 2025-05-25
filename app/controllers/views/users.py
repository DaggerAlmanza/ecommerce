from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from typing import Annotated

from app.controllers.serializers.response import (
    Response as ResponseSerializer
)
from app.controllers.serializers.users import (
    User as userSerializer,
)
from app.services.users import UserService
from app.controllers.views.authenticate import get_current_user


router = APIRouter()
user_service = UserService()


@router.post(
    "/users",
    tags=["users"],
    response_model=ResponseSerializer
)
async def create_users(
    request: userSerializer,
):
    response = user_service.save(
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
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = user_service.update(
        id,
        request.model_dump(),
        current_user
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
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = user_service.get_by_id(id, current_user)
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
    response = user_service.get_all(current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.delete(
    "/users/{id}",
    tags=["users"],
    response_model=ResponseSerializer
)
async def delete_user(
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = user_service.delete_by_id(id, current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
