import aiohttp
import pytest
from dataclasses import dataclass
from multidict import CIMultiDictProxy
from elasticsearch import AsyncElasticsearch

SERVICE_URL = 'http://127.0.0.1:8000'
API_URL = f'{SERVICE_URL}/api/v1'

ES_HOST = '127.0.0.1'
ES_PORT = 9200


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{ES_HOST}:{ES_PORT}')
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: dict = None) -> HTTPResponse:
        params = params or {}
        url = API_URL + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status
            )
    return inner


@pytest.mark.asyncio
async def test_search_detailed(es_client):
    await es_client.bulk(...)
    response = await make_get_request('/search', {'search': 'Star Wars'})
    assert response.status == 200
    assert len(response.body) == 1
    # expected = {}
    # assert response.body == expected
