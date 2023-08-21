from aiohttp import web
import marshmallow

from mbc2.src.calculator import models


class Member(marshmallow.Schema):
    class Meta:
        unknown = marshmallow.INCLUDE

    name = marshmallow.fields.Str(required=True)
    paid = marshmallow.fields.Number(required=True)
    # for response only
    need_to_pay = marshmallow.fields.Number(required=True)

    @marshmallow.post_load
    def make_dc(self, data, **kwargs):
        return models.Member(**data)


class MembersBase:
    @marshmallow.validates('members')
    def _validate_members(self, value):
        if not value:
            raise marshmallow.ValidationError('required at least 1 member')

    @marshmallow.post_load
    def make_dc(self, data, **kwargs):
        return models.Members(**data)


class Request(marshmallow.Schema, MembersBase):
    class Meta:
        unknown = marshmallow.EXCLUDE

    members = marshmallow.fields.List(
        marshmallow.fields.Nested(Member(only=('name', 'paid'))),
        required=True,
    )


class Response(marshmallow.Schema, MembersBase):
    members = marshmallow.fields.List(
        marshmallow.fields.Nested(Member()),
        required=True,
    )


async def handler(request: web.Request) -> web.Response:
    # TODO: add csrf
    data = await request.json()
    members_dc: models.Members = Request().load(data)

    members_dc.calculate()

    return web.json_response(Response().dump(members_dc))
