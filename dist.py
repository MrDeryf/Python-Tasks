def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5


def test_distance():
    assert distance(4, 4, 4, 4) == 0.0