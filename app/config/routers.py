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

API_VERSION = "/api/v1"
urls = APIRouter()


urls.include_router(
    users.router,
    prefix=API_VERSION,
)

urls.include_router(
    carts.router,
    prefix=API_VERSION,
)

urls.include_router(
    products.router,
    prefix=API_VERSION,
)

urls.include_router(
    cart_items.router,
    prefix=API_VERSION,
)

urls.include_router(
    order_items.router,
    prefix=API_VERSION,
)

urls.include_router(
    orders.router,
    prefix=API_VERSION,
)

urls.include_router(
    authenticate.router,
)
