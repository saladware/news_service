from fastapi import APIRouter


news = APIRouter(prefix='/news', tags=['news'])


@news.get('/{news_id}')
async def get_news_by_id():
    ...
