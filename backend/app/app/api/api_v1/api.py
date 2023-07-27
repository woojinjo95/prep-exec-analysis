from fastapi import APIRouter

from app.api.api_v1.endpoints import item, remocon

api_router = APIRouter()
api_router.include_router(item.router, prefix="/item", tags=["item"])
api_router.include_router(remocon.router, prefix="/remocon", tags=["remocon"])
