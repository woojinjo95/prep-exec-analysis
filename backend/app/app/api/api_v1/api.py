from app.api.api_v1.endpoints import item, remocon, scenario, hardware_configuration, block, stb_connection
from fastapi import APIRouter

api_router = APIRouter()
# api_router.include_router(item.router, prefix="/item", tags=["item"])
api_router.include_router(hardware_configuration.router, prefix="/hardware_configuration", tags=["settings"])
api_router.include_router(stb_connection.router, prefix="/stb_connection", tags=["settings"])
api_router.include_router(remocon.router, prefix="/remocon", tags=["remocon"])
api_router.include_router(scenario.router, prefix="/scenario", tags=["scenario"])
api_router.include_router(block.router, prefix="/scenario/block", tags=["scenario"])
api_router.include_router(block.router_detail, prefix="/scenario/block_group", tags=["scenario"])
