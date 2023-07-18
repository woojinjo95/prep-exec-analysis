from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings


def init_db(db: Session) -> None:
    user_id = settings.FIRST_SUPERUSER
    if crud.user.get_by_user_id(db, user_id=user_id) is None:
        user_in = schemas.UserCreate(
            user_id=user_id,
            password=settings.FIRST_SUPERUSER_PASSWORD)
        crud.user.create(db, obj_in=user_in)
