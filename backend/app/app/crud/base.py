from enum import Enum
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from app.db.base_class import Base
from app.fastapi_pagination import Page
from app.fastapi_pagination.ext.sqlalchemy import init_query_to_dict, paginate
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Query, Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session
    ) -> List[ModelType]:
        return db.query(self.model).all()

    def get_multi_paginate(
        self, db: Session
    ) -> Page[ModelType]:
        return paginate(db.query(self.model))

    def get_multi_or_paginate_by_query(
        self, query: Query, page: Optional[int] = 0
    ) -> Page[ModelType]:
        if page:
            res = paginate(query)
        else:
            res = init_query_to_dict(query)
        return res

    def schema_encoder(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        return db_obj

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.schema_encoder(db, obj_in=obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_flush(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.schema_encoder(db, obj_in=obj_in)
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj

    def update_encoder(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                field_data = update_data[field]
                if isinstance(update_data[field], Enum):
                    field_data = field_data.value
                setattr(db_obj, field, field_data)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        db_obj = self.update_encoder(db, db_obj=db_obj, obj_in=obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
