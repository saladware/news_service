from sqlalchemy import Column, Text, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base


class News(Base):
    __tablename__ = 'news'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey)