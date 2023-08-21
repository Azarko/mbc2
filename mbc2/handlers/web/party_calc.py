from aiohttp import web
import aiohttp_jinja2


async def handler(request: web.Request) -> web.Response:
    data = {'active_tab': 'party_calc'}
    return await aiohttp_jinja2.render_template_async(
        'party_calc_index.html',
        request,
        data,
    )
