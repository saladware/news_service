from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_news_by_id(session: AsyncSession, news_id: UUID):
    query = select(News)