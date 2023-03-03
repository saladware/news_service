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
