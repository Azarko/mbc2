import json

from aiohttp import web
import marshmallow.exceptions


@web.middleware
async def catch_validation_error(request, handler):
    """Catch marshmallow ValidationError and transform it to 400 response."""
    try:
        return await handler(request)
    except marshmallow.exceptions.ValidationError as err:
        key, values = err.messages.popitem()
        message = f'{key}: {", ".join(values)}'
        raise web.HTTPBadRequest(
            body=json.dumps({'code': 'VALIDATION_ERROR', 'message': message}),
            content_type='application/json',
        )


@web.middleware
async def ajax_csrf_token(request, handler):
    """Custom request header csrf policy."""
    if request.method in ('POST', 'PATCH', 'DELETE', 'PUT'):
        if not request.headers.get('X-Mbc-Csrf-Token'):
            raise web.HTTPForbidden(
                body=json.dumps(
                    {'code': 'CSRF_ERROR', 'message': 'csrf error'},
                ),
                content_type='application/json',
            )
    return await handler(request)
