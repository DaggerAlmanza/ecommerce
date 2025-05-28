from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from typing import Annotated

from app.controllers.serializers.orders import Orders as OrdersSerializer
from app.controllers.serializers.response import (
    Response as ResponseSerializer,
)
from app.controllers.views.authenticate import get_current_user
from app.services.orders import OrdersService


router = APIRouter()
orders_service = OrdersService()


@router.post(
    "/orders",
    tags=["orders"],
    response_model=ResponseSerializer
)
async def create_orders(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = orders_service.save_async(current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/orders",
    tags=["orders"],
    response_model=ResponseSerializer
)
async def get_all_orders(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = orders_service.get_all()
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/orders/tasks/{task_id}",
    tags=["orders"],
    response_model=ResponseSerializer
)
async def get_task_status(
    task_id: str,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = orders_service.get_task_status(task_id)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.put(
    "/orders/{id}",
    tags=["orders"],
    response_model=ResponseSerializer
)
async def update_orders(
    request: OrdersSerializer,
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = orders_service.update(
        id,
        request.model_dump()
    )
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/orders/{id}",
    tags=["orders"],
    response_model=ResponseSerializer
)
async def get_orders(
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = orders_service.get_by_id(id)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
