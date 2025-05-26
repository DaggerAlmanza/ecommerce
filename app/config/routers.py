from fastapi import APIRouter

from app.controllers.views import (
    authenticate,
    cart_items,
    carts,
    order_items,
    orders,
    products,
    users,
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
    order_items.router,
    prefix="/api/v1",
)

urls.include_router(
    orders.router,
    prefix="/api/v1",
)

urls.include_router(
    authenticate.router,
)
