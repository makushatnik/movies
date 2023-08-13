from functools import lru_cache
from typing import Optional, List
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from myfastapi.db.elastic import get_elastic
from myfastapi.db.redis import get_redis
from myfastapi.models.film import Film

from basic import BasicService

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService(BasicService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)

    async def get_all(self) -> List[Film]:
        result = []
        return result

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._get_from_cache(film_id)
        if not film:
            film = await self._get_from_elastic(film_id)
            if not film:
                return None
            await self._put_to_cache(film)
        return film

    async def _get_from_elastic(self, film_id: str) -> Optional[Film]:
        doc = await self.elastic.get('movies', film_id)
        return Film(**doc['_source'])

    async def _get_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        # film = Film.parse_raw(data)
        film = Film.model_validate_json(data)
        return film

    async def _put_to_cache(self, film: Film):
        await self.redis.set(film.id, film.model_dump_json(), ex=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    return FilmService(redis, elastic)
