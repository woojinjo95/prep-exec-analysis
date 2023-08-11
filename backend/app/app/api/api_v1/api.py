from app.api.api_v1.endpoints import item, remocon, scenario, hardware_configuration, block, file, client, analysis_config, trace, terminal, utility, analysis_result, workspace
from fastapi import APIRouter

api_router = APIRouter()
# api_router.include_router(item.router, prefix="/item", tags=["item"])
api_router.include_router(hardware_configuration.router, prefix="/hardware_configuration", tags=["hardware_configuration"])
api_router.include_router(remocon.router, prefix="/remocon", tags=["remocon"])
api_router.include_router(scenario.router, prefix="/scenario", tags=["scenario"])
api_router.include_router(block.router, prefix="/scenario/block", tags=["scenario"])
api_router.include_router(block.router_detail, prefix="/scenario/block_group", tags=["scenario"])
api_router.include_router(file.router, prefix="/file", tags=["file"])
api_router.include_router(analysis_config.router, prefix="/analysis_config", tags=["analysis_config"])
api_router.include_router(client.router, prefix="/client", tags=["client"])
api_router.include_router(trace.router, prefix="/trace", tags=["trace"])
api_router.include_router(terminal.router, prefix="/terminal", tags=["terminal"])
api_router.include_router(utility.router, prefix="/utility", tags=["utility"])
api_router.include_router(analysis_result.router, prefix="/analysis_result", tags=["analysis_result"])
api_router.include_router(workspace.router, prefix="/workspace", tags=["workspace"])
