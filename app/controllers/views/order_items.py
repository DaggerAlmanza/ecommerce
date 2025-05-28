from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from typing import Annotated

from app.controllers.serializers.response import (
    Response as ResponseSerializer,
)
from app.services.order_items import OrderItemsService
from app.controllers.views.authenticate import get_current_user


router = APIRouter()
order_items_service = OrderItemsService()


@router.get(
    "/order_items",
    tags=["order_items"],
    response_model=ResponseSerializer
)
async def get_all_order_items(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = order_items_service.get_all()
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/order_items/user",
    tags=["order_items"],
    response_model=ResponseSerializer
)
async def get_all_order_items_by_user(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = order_items_service.get_all_by_user(current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/order_items/{id}",
    tags=["order_items"],
    response_model=ResponseSerializer
)
async def get_order_items(
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = order_items_service.get_by_id(id)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
