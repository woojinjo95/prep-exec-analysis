import logging
import traceback

from app import crud, schemas
from app.api import deps
from app.models import User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
router = APIRouter()


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> schemas.User:
    """
    Update a user.
    """
    try:
        user = crud.user.get(db, id=user_id)
        if not user:
            raise HTTPException(status_code=404,
                                detail="The user with this user does not exist in the system")
        user_in.updated_by_id = current_user.id
        user = crud.user.update(db, db_obj=user, obj_in=user_in)
    except SQLAlchemyError as e:
        logger.error(f'error: {e} {traceback.format_exc()}')
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return user
