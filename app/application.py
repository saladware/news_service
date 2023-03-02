from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .exceptions import ItemNotFound, ItemAlreadyExists, APIException
from .users.router import users
from .news.router import news


app = FastAPI(
    title='News Web Service'
)


@app.exception_handler(APIException)
async def on_not_found(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.code,
        content={'detail': exc.detail if len(exc.args) == 0 else exc.args[0]}
    )


app.include_router(users)
app.include_router(news)
