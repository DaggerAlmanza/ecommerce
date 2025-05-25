from fastapi import APIRouter

from app.controllers.views import (
    users,
    authenticate,
    carts,
    cart_items,
    products,
)

urls = APIRouter()


urls.include_router(
    users.router,
    prefix="/api/v1",
)

urls.include_router(
    carts.router,
    prefix="/api/v1",
)

urls.include_router(
    products.router,
    prefix="/api/v1",
)

urls.include_router(
    cart_items.router,
    prefix="/api/v1",
)

urls.include_router(
    authenticate.router,
)
