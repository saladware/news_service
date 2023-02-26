from sqlalchemy import Column, Text, String, text, Enum, DateTime, func, Date
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base
from .schemas import Gender


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    email = Column(String(320), nullable=False, unique=True, index=True)
    fullname = Column(Text, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    birthday = Column(Date, nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    hashed_password = Column(Text, nullable=False)
