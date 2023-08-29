from app.api.api_v1.endpoints import remocon, scenario, hardware_configuration, block, file, client, analysis_config, trace, shell, utility, analysis_result, testrun, scenario_tag
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(hardware_configuration.router, prefix="/hardware_configuration",
                          tags=["hardware_configuration"])
api_router.include_router(remocon.router, prefix="/remocon", tags=["remocon"])

api_router.include_router(scenario_tag.router, prefix="/scenario/tag", tags=["scenario:tag"])
api_router.include_router(testrun.router, prefix="/scenario/testrun", tags=["scenario:testrun"])
api_router.include_router(scenario.router, prefix="/scenario", tags=["scenario"])
api_router.include_router(scenario.router_detail, prefix="/copy_scenario", tags=["scenario"])
api_router.include_router(block.router, prefix="/scenario/block", tags=["scenario:block"])
api_router.include_router(block.router_detail, prefix="/scenario/blocks", tags=["scenario:block"])
api_router.include_router(block.block_group_router, prefix="/scenario/block_group", tags=["scenario:block"])

api_router.include_router(analysis_config.router, prefix="/analysis_config", tags=["analysis_config"])

api_router.include_router(trace.router, prefix="/trace", tags=["trace"])
api_router.include_router(shell.router, prefix="/shell", tags=["shell"])
api_router.include_router(analysis_result.router, prefix="/analysis_result", tags=["analysis_result"])

api_router.include_router(file.router, prefix="/file", tags=["file"])

api_router.include_router(utility.router, tags=["default"])
api_router.include_router(client.router, prefix="/client", tags=["default"])
