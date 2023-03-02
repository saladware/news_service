from uuid import UUID

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from . import service
from .models import User
from .service import oauth2_scheme
from ..database import get_session
from ..config import SECRET_K, ALGORITHM
from ..exceptions import AccessDenied


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_K, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await service.get_user_by_id(session, UUID(user_id))
    return user


async def can_user_edit(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> User:
    if current_user.id == user_id:
        return current_user
    if current_user.role == "ADMIN":
        return await service.get_user_by_id(db, user_id)
    raise AccessDenied("you are not this user or admin")


can_user_delete = can_user_edit
