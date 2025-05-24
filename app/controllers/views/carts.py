from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from typing import Annotated

from app.controllers.serializers.response import (
    Response as ResponseSerializer
)
from app.services.carts import CartService
from app.controllers.views.authenticate import get_current_user


router = APIRouter()
cart_service = CartService()


@router.post(
    "/carts",
    tags=["carts"],
    response_model=ResponseSerializer
)
async def create_carts(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_service.save(current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/carts/{id}",
    tags=["carts"],
    response_model=ResponseSerializer
)
async def get_carts(
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_service.get_by_id(id, current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/carts",
    tags=["carts"],
    response_model=ResponseSerializer
)
async def get_all_carts(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_service.get_all(current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
