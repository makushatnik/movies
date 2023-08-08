import aiohttp
from aiohttp import web
from aiohttp.web import Request, StreamResponse

REMOTE_URL = 'https://fish-text.ru/get'


async def get_phrase():
    async with aiohttp.ClientSession() as session:
        async with session.get(REMOTE_URL, params={'type': 'title'}) as response:
            result = await response.json(content_type='text/html; charset=utf-8')
            return result.get('text')


async def index_handler(request):
    return web.Response(text=await get_phrase())


async def response_signal(request: Request, response: StreamResponse) -> StreamResponse | None:
    response.text = response.text.upper()
    return response


async def make_app():
    app = web.Application()
    app.on_response_prepare.append(response_signal)
    app.add_routes([web.get('/', index_handler)])
    return app


web.run_app(make_app())


