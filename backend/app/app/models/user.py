from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, comment='아이디')
    user_id = Column(String(10), unique=True, nullable=False, comment='사용자 아이디')
    password = Column(String(100), nullable=False, comment='비밀번호')
    updated_at = Column(DateTime(timezone=True), nullable=False,
                        default=func.now(), onupdate=func.now(), comment='변경일시')
