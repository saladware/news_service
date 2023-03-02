from datetime import timedelta, datetime
from uuid import UUID

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from .models import User
from . import schemas
from ..config import SECRET_K, ALGORITHM
from ..exceptions import ItemNotFound, ItemAlreadyExists, AccessDenied, Unauthorized

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User:
    query = select(User).where(User.id == user_id).limit(1)
    result: Result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise ItemNotFound("user with this id is not found")
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    query = select(User).where(User.email == email).limit(1)
    result: Result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise ItemNotFound("user with this email is not found")
    return user


async def create_user(session: AsyncSession, data: schemas.RegisterUser) -> User:
    user = User(
        **data.dict(exclude={"password"}), hashed_password=hash_password(data.password)
    )
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise ItemAlreadyExists("user with this email is already exists")
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, user: User, data: schemas.UpdateUser):
    for key, value in data.dict(exclude_none=True).items():
        setattr(user, key, value)
    try:
        await session.commit()
    except IntegrityError:
        raise ItemAlreadyExists("user with this email is already exists")
    await session.refresh(user)


async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.commit()


def check_password(password: str, user: User):
    if not verify_password(password, user.hashed_password):
        raise Unauthorized("wrong password")


async def change_password(
    session: AsyncSession, user: User, data: schemas.ChangePassword
):
    check_password(data.old_password, user)
    print(user.hashed_password)
    user.hashed_password = hash_password(data.new_password)
    await session.commit()
    print(user.hashed_password)


async def authenticate_user(session: AsyncSession, email: str, password: str) -> User:
    user = await get_user_by_email(session, email)
    check_password(password, user)
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_K, algorithm=ALGORITHM)
    return encoded_jwt
