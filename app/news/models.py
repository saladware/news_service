from sqlalchemy import (
    Column,
    Text,
    text,
    ForeignKey,
    DateTime,
    func,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    title = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    author_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tags = relationship(
        "NewsTag", back_populates="news", lazy="immediate", cascade="all"
    )
    comments = relationship(
        "Comment", back_populates="news", lazy="immediate", cascade="all"
    )


class NewsTag(Base):
    __tablename__ = "tags"
    __table_args__ = (UniqueConstraint("text", "news_id", name="_tag_content_uc"),)

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    text = Column(String(50), nullable=False)
    news_id = Column(UUID(as_uuid=True), ForeignKey("news.id"), nullable=False)

    news = relationship("News", back_populates="tags", lazy="immediate")

    def __str__(self):
        return self.text


class Comment(Base):
    __tablename__ = "comments"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    news_id = Column(UUID(as_uuid=True), ForeignKey("news.id"), nullable=False)

    news = relationship("News", back_populates="comments", lazy="immediate")
    author = relationship("User", lazy="immediate")
