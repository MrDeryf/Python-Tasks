def distance():
    x1 = int(input())
    y1 = int(input())
    x2 = int(input())
    y2 = int(input())
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5


def test_func(monkeypatch):
    inputs = [1, 2, 4, 6]

    def my_input():
        return inputs.pop()

    monkeypatch.setattr('builtins.input', my_input)
    assert distance() == 5.0
    print("It works")
