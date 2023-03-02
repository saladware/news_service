from sqlalchemy import Column, Text, DateTime, text, func
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    news_id = Column(UUID(as_uuid=True))
    author_id = Column(UUID(as_uuid=True))
