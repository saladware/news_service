from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .models import News
from ..database import get_session
from ..users.dependencies import get_current_user
from ..users.models import User
from . import service
from ..exceptions import AccessDenied


async def can_edit_news(
    news_id: UUID, user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)
) -> News:
    news = await service.get_news_by_id(session, news_id)
    if news.author_id != user.id and user.role != "ADMIN":
        raise AccessDenied("you are not author of this news")
    return news


can_delete_news = can_edit_news
