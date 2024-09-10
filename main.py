import logging

import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from api import api_router
from core.config import uvicorn_options
from core.logger import LOGGING_CONFIG
from db.db import db_dependency


logging.config.dictConfig(LOGGING_CONFIG)
app = FastAPI(docs_url="/api/openapi")
app.include_router(api_router)


@app.get('/ping', tags=['database'])
async def ping(db: db_dependency):
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        **uvicorn_options
    )
