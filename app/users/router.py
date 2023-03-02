from datetime import timedelta
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from . import service, schemas
from .dependencies import get_current_user
from .models import User
from .service import create_access_token
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..database import get_session

users = APIRouter(prefix='/users', tags=['users'])


@users.get('/me')
async def get_me(user: User = Depends(get_current_user)) -> schemas.User:
    return user


@users.get('/{user_id}')
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_session)) -> schemas.User:
    return await service.get_user_by_id(db, user_id)


@users.post('/')
async def register_new_user(data: schemas.RegisterUser, db: AsyncSession = Depends(get_session)) -> schemas.User:
    return await service.create_user(db, data)


@users.put('/me')
async def change_me(data: schemas.UpdateUser, user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_session)) -> schemas.User:
    await service.update_user(db, user, data)
    return user


@users.delete('/me')
async def delete_me(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    await service.delete_user(db, user)
    return {'detail': 'success'}


@users.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: AsyncSession = Depends(get_session)) -> schemas.Token:
    user = await service.authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type='bearer')


@users.put('/password')
async def change_password(data: schemas.ChangePassword, user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_session)):
    await service.change_password(db, user, data)
    return {'detail': 'success'}
