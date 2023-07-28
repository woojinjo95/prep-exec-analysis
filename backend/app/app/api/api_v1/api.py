from fastapi import APIRouter

from app.api.api_v1.endpoints import item, hardware_configuration

api_router = APIRouter()
api_router.include_router(item.router, prefix="/item", tags=["item"])
api_router.include_router(hardware_configuration.router, prefix="/hardware_configuration", tags=["hardware_configuration"])
