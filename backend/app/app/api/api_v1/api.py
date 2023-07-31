from app.api.api_v1.endpoints import item, remocon,  scenario, hardware_configuration, file
from fastapi import APIRouter

api_router = APIRouter()
# api_router.include_router(item.router, prefix="/item", tags=["item"])
api_router.include_router(scenario.router, prefix="/scenario", tags=["scenario"])
api_router.include_router(remocon.router, prefix="/remocon", tags=["remocon"])
api_router.include_router(hardware_configuration.router, prefix="/hardware_configuration", tags=["hardware_configuration"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
