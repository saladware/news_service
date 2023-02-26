from fastapi import APIRouter


users = APIRouter(prefix='/users', tags=['users'])


@users.get('/{user_id}')
async def get_user_by_id():
    ...
