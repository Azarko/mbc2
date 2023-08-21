import pytest

from mbc2.src.calculator import models


@pytest.mark.parametrize(
    ('paid_list', 'expected_avg'),
    (
        pytest.param((2, 2), 2, id='OK-integer'),
        pytest.param((1, 2), 1.5, id='OK-float'),
        pytest.param(
            (0, 2, 3),
            1.67,
            id='round',
        ),
        pytest.param((), 0, id='zero division'),
    ),
)
def test_avg_paid(paid_list, expected_avg):
    members = models.Members(
        [models.Member(name='test', paid=paid) for paid in paid_list],
    )
    assert members.avg_paid == expected_avg


@pytest.mark.parametrize(
    ('paid_list', 'expected_need_to_pay'),
    (
        pytest.param((1, 2), (0.5, -0.5), id='OK'),
        pytest.param(
            (1, 3, 1),
            (0.67, -1.33, 0.67),
            id='rounding',
        ),
        pytest.param((), (), id='no data'),
        pytest.param((10, 10), (0, 0), id='same paid'),
    ),
)
def test_calculate(paid_list, expected_need_to_pay):
    members = models.Members(
        [models.Member(name='test', paid=paid) for paid in paid_list],
    )
    members.calculate()
    assert (
        tuple(member.need_to_pay for member in members.members)
        == expected_need_to_pay
    )
