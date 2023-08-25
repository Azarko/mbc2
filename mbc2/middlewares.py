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
            text=json.dumps({'code': 'VALIDATION_ERROR', 'message': message}),
        )
