from uuid import UUID

from sqlalchemy import select, insert
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import ItemNotFound, ItemAlreadyExists
from app.news import schemas
from app.news.models import News, NewsTag, Comment
from app.users.models import User


async def get_news_by_id(session: AsyncSession, news_id: UUID) -> News:
    query = select(News).where(News.id == news_id).limit(1)
    result: Result = await session.execute(query)
    news = result.scalar_one_or_none()
    if news is None:
        raise ItemNotFound("news with this id is not found")
    return news


async def create_news(
    session: AsyncSession, data: schemas.CreateNews, author: User
) -> News:
    news = News(**data.dict(exclude={"tags"}), author_id=author.id)
    session.add(news)
    try:
        await session.commit()
    except IntegrityError:
        raise ItemAlreadyExists("news with this title already exists")
    if data.tags:
        session.add_all(
            [NewsTag(text=name, news_id=news.id) for name in set(data.tags)]
        )
        await session.commit()
    await session.refresh(news)
    return news


async def update_news(
    session: AsyncSession, data: schemas.UpdateNews, news_object: News
):
    for key, value in data.dict(exclude_none=True).items():
        setattr(news_object, key, value)
    try:
        await session.commit()
    except IntegrityError:
        raise ItemAlreadyExists("news with this title already exists")
    await session.commit()
    await session.refresh(news_object)


async def delete_news(session: AsyncSession, news_object: News()):
    await session.delete(news_object)
    await session.commit()


async def add_tag(session: AsyncSession, news: News, tag: str) -> NewsTag:
    tag = NewsTag(text=tag, news_id=news.id)
    session.add(tag)
    try:
        await session.commit()
    except IntegrityError:
        raise ItemAlreadyExists(f"tag with this name already exists")
    await session.refresh(tag)
    return tag


async def delete_tag(session: AsyncSession, tag_id: UUID):
    query = select(NewsTag).where(NewsTag.id == tag_id).limit(1)
    result = await session.execute(query)
    tag = result.scalar_one_or_none()
    if tag is None:
        raise ItemNotFound("tag with this name is not found")
    await session.delete(tag)
    await session.commit()


async def get_news_tags(session: AsyncSession, news_id: UUID):
    news = await get_news_by_id(session, news_id)
    return news.tags


async def get_users_news(session: AsyncSession, user: User) -> list[News]:
    query = select(News).where(News.author_id == user.id)
    result = await session.execute(query)
    return list(result.scalars())


async def get_all_news(session: AsyncSession) -> list[News]:
    query = select(News)
    result = await session.execute(query)
    return list(result.scalars())


async def create_comment(
    session: AsyncSession, news_id, author: User, data: schemas.CreateComment
) -> Comment:
    news = await get_news_by_id(session, news_id)
    comment = Comment(author_id=author.id, news_id=news.id, content=data.content)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment


async def get_news_comments(session, news_id: UUID) -> list[Comment]:
    news = await get_news_by_id(session, news_id)
    query = select(Comment).where(Comment.news_id == news.id)
    result = await session.execute(query)
    return list(result.scalars())


async def get_comment(session: AsyncSession, comment_id: UUID) -> Comment:
    query = select(Comment).where(Comment.id == comment_id).limit(1)
    result: Result = await session.execute(query)
    comment = result.scalar_one_or_none()
    if comment is None:
        raise ItemNotFound("comment with this id is not found")
    return comment


async def edit_comment(session: AsyncSession, comment_id: UUID, data: schemas.EditComment) -> Comment:
    comment = await get_comment(session, comment_id)
    comment.content = data.content
    await session.commit()
    await session.refresh(comment)
    return comment


async def delete_comment(session: AsyncSession, comment_id: UUID):
    comment = await get_comment(session, comment_id)
    await session.delete(comment)
    await session.commit()


async def get_users_comments(session: AsyncSession, user: User) -> list[Comment]:
    query = select(Comment).where(Comment.author_id == user.id)
    result = await session.execute(query)
    return list(result.scalars())