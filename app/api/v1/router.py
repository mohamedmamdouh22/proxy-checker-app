"""API v1 router that combines all endpoint routers."""
from fastapi import APIRouter

from app.api.v1.endpoints import proxy

api_router = APIRouter()

# Include proxy endpoints
api_router.include_router(
    proxy.router,
    prefix="/proxy",
    tags=["proxy"],
)
