from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from .models import User
from . import schemas
from ..exceptions import ItemNotFound, ItemAlreadyExists


def hash_password(password: str) -> str:
    import base64
    return base64.b64encode(password.encode()).decode()


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User:
    query = select(User).where(User.id == user_id).limit(1)
    result: Result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise ItemNotFound('user with this id is not found')
    return user


async def create_user(session: AsyncSession, data: schemas.RegisterUser) -> User:
    user = User(**data.dict(exclude={'password'}), hashed_password=hash_password(data.password))
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise ItemAlreadyExists('user with this email is already exists')
    await session.refresh(user)
    return user


async def update_user_by_id(session: AsyncSession, user_id: UUID, data: schemas.UpdateUser) -> User:
    user = await get_user_by_id(session, user_id)
    for key, value in data.dict(exclude_none=True).items():
        setattr(user, key, value)
    try:
        await session.commit()
    except IntegrityError:
        raise ItemAlreadyExists('user with this email is already exists')
    await session.refresh(user)
    return user


async def delete_user_by_id(session: AsyncSession, user_id: UUID):
    user = await get_user_by_id(session, user_id)
    await session.delete(user)
    await session.commit()
