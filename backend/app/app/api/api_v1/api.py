from app.api.api_v1.endpoints import action_block, remocon
from fastapi import APIRouter

api_router = APIRouter()
# api_router.include_router(item.router, prefix="/item", tags=["item"])
api_router.include_router(
    action_block.router, prefix="/action_block", tags=["action_block"])
api_router.include_router(remocon.router, prefix="/remocon", tags=["remocon"])
