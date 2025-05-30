from fastapi import APIRouter, Depends, UploadFile
from starlette.responses import JSONResponse
from typing import Annotated

from app.controllers.serializers.response import (
    Response as ResponseSerializer,
)
from app.controllers.serializers.products import (
    Products as ProductsSerializer,
    ProductsUpdate as ProductsUpdateSerializer
)
from app.services.products import ProductsService
from app.controllers.views.authenticate import get_current_user


router = APIRouter()
products_service = ProductsService()


@router.post(
    "/products",
    tags=["products"],
    response_model=ResponseSerializer
)
async def create_products(
    request: ProductsSerializer,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = products_service.save(current_user, request.model_dump())
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.post(
    "/products/upload_file",
    tags=["products"],
    response_model=ResponseSerializer
)
async def create_image_url(
    file: UploadFile,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = products_service.image_url(file)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/products/admin",
    tags=["admin"],
    response_model=ResponseSerializer
)
async def get_all_products_deleted(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = products_service.get_all_deleted(current_user)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/products/{id}",
    tags=["products"],
    response_model=ResponseSerializer
)
async def get_products(
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = products_service.get_by_id(id)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/products",
    tags=["products"],
    response_model=ResponseSerializer
)
async def get_all_products(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = products_service.get_all()
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.put(
    "/products/{id}",
    tags=["products"],
    response_model=ResponseSerializer
)
async def update_products(
    request: ProductsUpdateSerializer,
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = products_service.update(
        current_user,
        id,
        request.model_dump()
    )
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.delete(
    "/products/{id}",
    tags=["products"],
    response_model=ResponseSerializer
)
async def delete_products(
    id: int,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = products_service.delete_by_id(current_user, id)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
