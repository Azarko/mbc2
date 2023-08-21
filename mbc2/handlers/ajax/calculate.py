import dataclasses
import logging
import typing

from aiohttp import web
import marshmallow

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class MemberData:
    name: str
    paid: float


@dataclasses.dataclass
class MembersData:
    members: typing.List[MemberData]


class Member(marshmallow.Schema):
    class Meta:
        unknown = marshmallow.INCLUDE

    name = marshmallow.fields.Str(required=True)
    paid = marshmallow.fields.Number(required=True)

    @marshmallow.post_load
    def make_dc(self, data, **kwargs):
        return MemberData(**data)


class Request(marshmallow.Schema):
    class Meta:
        unknown = marshmallow.EXCLUDE

    members = marshmallow.fields.List(
        marshmallow.fields.Nested(Member()),
        required=True,
    )

    @marshmallow.validates('members')
    def _validate_members(self, value):
        if not value:
            raise marshmallow.ValidationError('required at least 1 member')

    @marshmallow.post_load
    def make_dc(self, data, **kwargs):
        return MembersData(**data)


async def handler(request: web.Request) -> web.Response:
    # TODO: add csrf
    data = await request.json()
    members_dc: MembersData = Request().load(data)
    for member in members_dc.members:
        logger.info(member)

    # TODO: add calculate logic =)

    # TODO: validate response
    return web.json_response(
        {
            'members': [
                {
                    'name': member.name,
                    'paid': member.paid,
                    'need_to_pay': -member.paid,
                }
                for member in members_dc.members
            ],
        },
    )
