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


def _create_members_response(members: typing.List) -> typing.Dict:
    return {'members': members}


def _create_pytest_param(
    *,
    test_id: str,
    members: typing.List,
    expected_code: http.HTTPStatus = http.HTTPStatus.OK,
    expected_response: typing.Dict,
) -> typing.Any:
    return pytest.param(
        members,
        expected_code,
        expected_response,
        id=test_id,
    )


@pytest.mark.parametrize(
    ('members', 'expected_code', 'expected_response'),
    (
        _create_pytest_param(
            members=[_create_member(paid=50), _create_member()],
            expected_response=_create_members_response(
                [
                    _create_member(paid=50, need_to_pay=25),
                    _create_member(need_to_pay=-25),
                ],
            ),
            test_id='OK',
        ),
        _create_pytest_param(
            members=[_create_member()],
            expected_response=_create_members_response(
                [_create_member(need_to_pay=0)],
            ),
            test_id='one member',
        ),
        _create_pytest_param(
            members=[_create_member(), _create_member()],
            expected_response=_create_members_response(
                [_create_member(need_to_pay=0), _create_member(need_to_pay=0)],
            ),
            test_id='same values',
        ),
        _create_pytest_param(
            members=[
                _create_member(paid=1),
                _create_member(paid=3),
                _create_member(paid=1),
            ],
            expected_response=_create_members_response(
                [
                    _create_member(paid=1.0, need_to_pay=0.67),
                    _create_member(paid=3.0, need_to_pay=-1.33),
                    _create_member(paid=1.0, need_to_pay=0.67),
                ],
            ),
            test_id='rounding',
        ),
        _create_pytest_param(
            members=[],
            expected_code=http.HTTPStatus.BAD_REQUEST,
            expected_response={
                'code': 'VALIDATION_ERROR',
                'message': 'members: required at least 1 member',
            },
            test_id='validation-error',
        ),
    ),
)
async def test_calculate(
    web_app_client,
    members,
    expected_code,
    expected_response,
):
    response = await web_app_client.post(
        '/party-calc/calculate',
        json={'members': members},
        headers={'X-Mbc-Csrf-Token': '1'},
    )
    body = await response.json()
    assert response.status == expected_code

    assert body == expected_response


async def test_calculate_no_csrf(web_app_client):
    response = await web_app_client.post(
        '/party-calc/calculate',
        json={'members': [_create_member()]},
    )
    assert response.status == http.HTTPStatus.FORBIDDEN
    body = await response.json()
    assert body == {'code': 'CSRF_ERROR', 'message': 'csrf error'}
