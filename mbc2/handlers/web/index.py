from aiohttp import web
import aiohttp_jinja2


async def handler(request: web.Request) -> web.Response:
    data = {'name': 'world', 'active_tab': 'index'}
    return await aiohttp_jinja2.render_template_async(
        'index.html',
        request,
        data,
    )
