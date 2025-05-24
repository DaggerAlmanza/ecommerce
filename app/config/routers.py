from fastapi import APIRouter

from app.controllers.views import (
    users,
    authenticate
)

urls = APIRouter()


urls.include_router(
    users.router,
    prefix="/api/v1",
)

urls.include_router(
    authenticate.router,
)
