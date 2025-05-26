from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from typing import Annotated

from app.controllers.serializers.response import (
    Response as ResponseSerializer
)
from app.controllers.serializers.cart_items import (
    CartItems as CartItemsSerializer,
    CartItemsUpdate as CartItemsUpdateSerializer
)
from app.services.cart_items import CartItemsService
from app.controllers.views.authenticate import get_current_user


router = APIRouter()
cart_items_service = CartItemsService()


@router.post(
    "/cart_items",
    tags=["cart_items"],
    response_model=ResponseSerializer
)
async def create_cart_items(
    request: CartItemsSerializer,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_items_service.save(current_user, request.model_dump())
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/cart_items/{id}",
    tags=["cart_items"],
    response_model=ResponseSerializer
)
async def get_cart_items(
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_items_service.get_by_id(id, current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/cart_items",
    tags=["cart_items"],
    response_model=ResponseSerializer
)
async def get_all_cart_items(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_items_service.get_all(current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/cart_items/admin",
    tags=["admin"],
    response_model=ResponseSerializer
)
async def get_all_cart_items_by_admin(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_items_service.get_all_by_admin(current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.put(
    "/cart_items/{id}",
    tags=["cart_items"],
    response_model=ResponseSerializer
)
async def update_cart_items(
    request: CartItemsUpdateSerializer,
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_items_service.update(
        current_user,
        id,
        request.model_dump()
    )
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.delete(
    "/cart_items/{id}",
    tags=["cart_items"],
    response_model=ResponseSerializer
)
async def delete_cart_items(
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = cart_items_service.delete_by_id(current_user, id)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
