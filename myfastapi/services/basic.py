from aioredis import Redis
from elasticsearch import AsyncElasticsearch


class BasicService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
