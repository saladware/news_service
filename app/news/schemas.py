from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateNews(BaseModel):
    title: str
    description: str
    tags: list[str] | None


class NewsTag(BaseModel):
    id: UUID
    text: str

    class Config:
        orm_mode = True


class CreateNewsTag(BaseModel):
    text: str


class News(BaseModel):
    id: UUID
    title: str
    description: str
    author_id: UUID
    created_at: datetime
    tags: list[NewsTag] | None

    class Config:
        orm_mode = True


class UpdateNews(BaseModel):
    title: str | None
    description: str | None


class NewsList(BaseModel):
    news: list[News]


class CreateComment(BaseModel):
    content: str


class Comment(BaseModel):
    id: UUID
    content: str
    created_at: datetime
    news_id: UUID
    author_id: UUID

    class Config:
        orm_mode = True


class CommentList(BaseModel):
    comments: list[Comment]


class EditComment(BaseModel):
    content: str
