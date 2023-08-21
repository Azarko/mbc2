import pytest

from mbc2.src.calculator import models


@pytest.mark.parametrize(
    ('paid', 'each_pay', 'expected_payment'),
    (
        pytest.param(10, 5, -5, id='OK'),
        pytest.param(
            1.2,
            0.1,
            -1.1,
            id='floating-point',
        ),
        pytest.param(
            10,
            10 / 3,
            -6.67,
            id='rounding',
        ),
    ),
)
def test_calculate(paid, each_pay, expected_payment):
    member = models.Member(name='test', paid=paid)
    member.calculate(each_pay)
    assert member.need_to_pay == expected_payment
