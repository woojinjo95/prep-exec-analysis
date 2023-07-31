import logging

from app import schemas
from app.crud.base import load_from_mongodb
from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=schemas.Scenario)
def read_scenario() -> schemas.Scenario:
    """
    Retrieve scenario.
    """
    res = load_from_mongodb(col='scenario')
    return {'items': res[0] if res else {}}
