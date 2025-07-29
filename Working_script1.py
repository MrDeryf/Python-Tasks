import pytest
import deal


@deal.pre(lambda x1, y1, x2, y2: isinstance(x1, float) and isinstance(y1, float) and isinstance(x2,
float) and isinstance(y2, float))
@deal.post(lambda result: result >= 0)
@deal.ensure(lambda x1, y1, x2, y2, result: result == ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)
@deal.reason(TypeError, lambda x1, x2, y1, y2: (not isinstance(x1, (float)) and not isinstance(y1, (float)) and not isinstance(x2, (
float)) and not isinstance(y2, (float))))
# @deal.raises(TypeError)
@deal.has()


def dist_new(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def test_dist_new():
    assert dist_new(0.0, 0.0, 3.0, 4.0) == 5.0

def test_dist_incorrect():
    with pytest.raises(deal.PreContractError):
        dist_new('7.0', 9, 3, 6)