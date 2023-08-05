from aiohttp import web


async def handler(request):
    return web.Response(text='Hello, world!')
