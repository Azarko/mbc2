import http
import typing

import pytest


def _create_member(
    name: str = 'test',
    paid: typing.Union[int, float] = 100,
    need_to_pay: typing.Union[int, float, None] = None,
) -> typing.Dict:
    result = {'name': name, 'paid': paid}
    if need_to_pay is not None:
        result['need_to_pay'] = need_to_pay
    return result


@pytest.mark.parametrize(
    ('members', 'expected_response'),
    (
        pytest.param(
            [_create_member(paid=50), _create_member()],
            [
                _create_member(paid=50, need_to_pay=25),
                _create_member(need_to_pay=-25),
            ],
            id='OK',
        ),
        pytest.param(
            [_create_member()],
            [_create_member(need_to_pay=0)],
            id='one member',
        ),
        pytest.param(
            [_create_member(), _create_member()],
            [_create_member(need_to_pay=0), _create_member(need_to_pay=0)],
            id='same values',
        ),
        pytest.param(
            [
                _create_member(paid=1),
                _create_member(paid=3),
                _create_member(paid=1),
            ],
            [
                _create_member(paid=1.0, need_to_pay=0.67),
                _create_member(paid=3.0, need_to_pay=-1.33),
                _create_member(paid=1.0, need_to_pay=0.67),
            ],
            id='rounding',
        ),
    ),
)
async def test_calculate(web_app_client, members, expected_response):
    response = await web_app_client.post(
        '/party-calc/calculate',
        json={'members': members},
    )
    body = await response.json()
    assert response.status == http.HTTPStatus.OK

    assert body['members'] == expected_response
