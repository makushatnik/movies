from functools import lru_cache
from typing import Optional, List
from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from myfastapi.db.elastic import get_elastic
from myfastapi.db.redis import get_redis
from myfastapi.models.genre import Genre

from basic import BasicService

GENRE_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService(BasicService):
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        super().__init__(redis, elastic)

    async def get_all(self) -> List[Genre]:
        result = []
        return result

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        genre = await self._get_from_cache(genre_id)
        if not genre:
            genre = await self._get_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_to_cache(genre)
        return genre

    async def _get_from_elastic(self, film_id: str) -> Optional[Genre]:
        doc = await self.elastic.get('movies', film_id)
        return Genre(**doc['_source'])

    async def _get_from_cache(self, film_id: str) -> Optional[Genre]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        # film = Genre.parse_raw(data)
        film = Genre.model_validate_json(data)
        return film

    async def _put_to_cache(self, film: Genre):
        await self.redis.set(film.id, film.model_dump_json(), ex=GENRE_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(redis, elastic)
