import logging
import json
import typing

from aiohttp import web


logger = logging.getLogger(__name__)


async def handler(request: web.Request):
    """
    request
    {
        "members": [
            {"name": "member_1", "paid: 100.00},
            {"name": "member_2", "paid": 0}
        ]
    }

    200
    {
        "members": [
            {"name": "member_1", "paid": 100, "need_pay": -50},
            {"name": "member_2", "paid": 0, "need_pay": 50}
        ]
    }
    """
    data = await request.json()
    logger.info(data)
    _validate_request(data)

    return web.json_response({'status': True})


def _validate_request(data: typing.Dict):
    members = data.get('members')
    if members is None:
        raise web.HTTPBadRequest(
            body=json.dumps(
                {
                    'code': 'VALIDATION_ERROR',
                    'message': 'members is required field',
                },
            ),
            content_type='application/json',
        )
    if not members:
        raise web.HTTPBadRequest(
            body=json.dumps(
                {
                    'code': 'VALIDATION_ERROR',
                    'message': 'members must have at least 1 element',
                },
            ),
            content_type='application/json',
        )
    for member in members:
        if 'name' not in member:
            raise web.HTTPBadRequest(
                body=json.dumps(
                    {
                        'code': 'VALIDATION_ERROR',
                        'message': 'name is required field',
                    },
                ),
                content_type='application/json',
            )
        if 'paid' not in member:
            raise web.HTTPBadRequest(
                body=json.dumps(
                    {
                        'code': 'VALIDATION_ERROR',
                        'message': 'paid is required field',
                    },
                ),
                content_type='application/json',
            )
        if not isinstance(member['paid'], float) and not isinstance(member['paid'], int):
            raise web.HTTPBadRequest(
                body=json.dumps(
                    {
                        'code': 'VALIDATION_ERROR',
                        'message': 'paid must be number',
                    },
                ),
                content_type='application/json',
            )
