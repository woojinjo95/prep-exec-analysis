import logging
import traceback
from datetime import timedelta
from typing import Any

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.core.security import verify_password
from app.db.redis_session import RedisClient
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/swagger-tokens", response_model=schemas.Token)
def auth_swagger(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        user = crud.user.get_by_user_id(db, user_id=form_data.username)
        access_token = security.create_access_token(
            user.id, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        RedisClient.hset(f'{access_token}', 'access', f'{user.id}')
        RedisClient.expire(f'{access_token}',
                           time=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)
    except SQLAlchemyError as e:
        logger.error(f'error: {e} {traceback.format_exc()}')
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {
        "access_token": access_token,
    }


@router.post("/tokens", response_model=schemas.Token)
def get_tokens(
    login_info: schemas.LoginInfo,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.get_by_user_id(db, user_id=login_info.user_id)
    if not user:
        raise HTTPException(status_code=404,
                            detail="The user with this user_id does not exist in the system")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    elif not verify_password(login_info.password, user.password):
        raise HTTPException(status_code=400,
                            detail={"msg": "The user with this password does not exist in the system"})

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires)
    refresh_token = security.create_refresh_token(
        user.id, expires_delta=refresh_token_expires)
    RedisClient.hset(f'{access_token}', 'access', f'{user.id}')
    RedisClient.expire(f'{access_token}',
                       time=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)
    RedisClient.hset(f'{refresh_token}', 'refresh', f'{user.id}')
    RedisClient.expire(f'{refresh_token}',
                       time=settings.REFRESH_TOKEN_EXPIRE_MINUTES*60)

    logger.info(f"login and creat access/refresh token")
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/token-refresh", response_model=schemas.AccessToken)
def token_refresh(
    token: str = Depends(deps.reusable_oauth2),
    current_user: models.User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
):
    refresh_token = RedisClient.hget(f'{token}', 'refresh')
    if not refresh_token:
        raise HTTPException(status_code=404, detail="refresh token not found")

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        current_user.id, expires_delta=access_token_expires)

    RedisClient.hset(f'{access_token}', 'access', f'{current_user.id}')
    RedisClient.expire(f'{access_token}',
                       time=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)
    logger.info("Reissue access token")
    return {
        "access_token": access_token,
    }


@router.delete('/revoke-tokens')
def revoke_tokens(
    token: str = Depends(deps.reusable_oauth2),
    current_user: models.User = Depends(deps.get_current_user),
):
    try:
        RedisClient.hdel(f'{token}', 'refresh')
        logger.info("revoke refresh token")
    except Exception as er:
        logger.error(f'error: {er} {traceback.format_exc()}')
        raise HTTPException(status_code=500, detail=traceback.format_exc())
    return {
        'detail': f"token deletion complete / Account id: {current_user.id}"
    }

@router.get("/me", response_model=schemas.User)
def read_me(
    _: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.User:
    """
    Get current user.
    """
    return current_user