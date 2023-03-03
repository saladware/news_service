from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.users.dependencies import get_current_user
from app.users.models import User

from . import service, schemas
from .dependencies import can_edit_news, can_delete_news
from .models import News

news = APIRouter(prefix="/news", tags=["news"])


@news.get("/my")
async def get_my_news(
    db: AsyncSession = Depends(get_session), author: User = Depends(get_current_user)
) -> schemas.NewsList:
    return schemas.NewsList(news=await service.get_users_news(db, author))


@news.get("/all")
async def get_all_news(db: AsyncSession = Depends(get_session)) -> schemas.NewsList:
    return schemas.NewsList(news=await service.get_all_news(db))


@news.get("/{news_id}")
async def get_news_by_id(
    news_id: UUID, db: AsyncSession = Depends(get_session)
) -> schemas.News:
    return await service.get_news_by_id(db, news_id)


@news.post("/")
async def create_news(
    data: schemas.CreateNews,
    author: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> schemas.News:
    return await service.create_news(db, data, author)


@news.put("/{news_id}")
async def change_news(
    data: schemas.UpdateNews,
    news_object: News = Depends(can_edit_news),
    db: AsyncSession = Depends(get_session),
) -> schemas.News:
    await service.update_news(db, data, news_object)
    return news_object


@news.delete("/{news_id}")
async def delete_news(
    news_object: News = Depends(can_delete_news),
    db: AsyncSession = Depends(get_session),
):
    await service.delete_news(db, news_object)
    return {"detail": "success"}


@news.get("/{news_id}/tags")
async def get_news_tags(
    news_id: UUID, db: AsyncSession = Depends(get_session)
) -> list[schemas.NewsTag]:
    return await service.get_news_tags(db, news_id)


@news.post("/{news_id}/tags")
async def add_tag(
    tag: str,
    news_object: News = Depends(can_edit_news),
    db: AsyncSession = Depends(get_session),
) -> schemas.NewsTag:
    return await service.add_tag(db, news_object, tag)


@news.delete("/{news_id}/tags/{tag_id}")
async def remove_tag(
    tag_id: UUID,
    _: News = Depends(can_edit_news),
    db: AsyncSession = Depends(get_session),
):
    await service.delete_tag(db, tag_id)
    return {"detail": "success"}


@news.post("/{news_id}/comments")
async def comment_news(
    news_id: UUID,
    data: schemas.CreateComment,
    author: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> schemas.Comment:
    return await service.create_comment(db, news_id, author, data)


@news.get("/{news_id}/comments")
async def get_news_comments(
    news_id: UUID, db: AsyncSession = Depends(get_session)
) -> schemas.CommentList:
    return schemas.CommentList(comments=await service.get_news_comments(db, news_id))


@news.get("/comments/my")
async def get_my_comments(
    author: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)
) -> schemas.CommentList:
    return schemas.CommentList(comments=await service.get_users_comments(db, author))


@news.get("/comments/{comment_id}")
async def get_comment_by_id(
    comment_id: UUID, db: AsyncSession = Depends(get_session)
) -> schemas.Comment:
    return await service.get_comment(db, comment_id)


@news.put("/comments/{comment_id}")
async def edit_comment_by_id(
    comment_id: UUID, data: schemas.EditComment, db: AsyncSession = Depends(get_session)
) -> schemas.Comment:
    return await service.edit_comment(db, comment_id, data)


@news.delete("/comments/{comment_id}")
async def edit_comment_by_id(comment_id: UUID, db: AsyncSession = Depends(get_session)):
    await service.delete_comment(db, comment_id)
    return {"detail": "success"}
