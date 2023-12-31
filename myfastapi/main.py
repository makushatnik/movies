import logging
import aioredis
import uvicorn as uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import film, genre
from core import config
from core.logger import LOGGING
from db import elastic
from db import redis

app = FastAPI(
    title=config.PROJECT_NAME,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    version="1.0.0"
)


# @app.on_event('startup')
# async def startup():
#     # Подключаемся к базам при старте сервера
#     redis.redis = await aioredis.create_redis_pool((config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20)
#     elastic.es = AsyncElasticsearch(hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'])
#
#
# @app.on_event('shutdown')
# async def shutdown():
#     # Отключаемся от баз при выключении сервера
#     await redis.redis.close()
#     await elastic.es.close()

app.include_router(film.router, prefix='/v1/film', tags=['Фильмы'])
app.include_router(genre.router, prefix='/v1/genre', tags=['Жанры'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=config.APP_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )
