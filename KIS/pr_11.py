class MealyError(Exception):
    pass


class Mealy:
    def __init__(self):
        self.state = "A"

    def reset(self):
        states = {"A": ("B", 0), "D": ("G", 5), "E": ("C", 7), "G": ("G", 11)}
        if self.state in states.keys():
            new_state, out = states[self.state]
            self.state = new_state
            return out
        raise MealyError("reset")

    def color(self):
        states = {"B": ("C", 1), "D": ("H", 4), "F": ("G", 8)}
        if self.state in states.keys():
            new_state, out = states[self.state]
            self.state = new_state
            return out
        raise MealyError("color")

    def warp(self):
        states = {
            "C": ("D", 2),
            "D": ("E", 3),
            "E": ("F", 6),
            "F": ("A", 9),
            "G": ("H", 10),
        }
        if self.state in states.keys():
            new_state, out = states[self.state]
            self.state = new_state
            return out
        raise MealyError("warp")


def main():
    return Mealy()


def test():
    o1 = main()
    try:  # A
        o1.color()
    except MealyError:
        pass
    try:  # A
        o1.warp()
    except MealyError:
        pass
    assert o1.reset() == 0
    try:  # B
        o1.reset()
    except MealyError:
        pass
    try:  # B
        o1.warp()
    except MealyError:
        pass
    assert o1.color() == 1
    try:  # C
        o1.reset()
    except MealyError:
        pass
    try:  # C
        o1.color()
    except MealyError:
        pass
    assert o1.warp() == 2
    assert o1.warp() == 3
    try:  # E
        o1.color()
    except MealyError:
        pass
    assert o1.reset() == 7
    test1(o1)


def test1(o1):
    o1.warp()
    o1.warp()
    assert o1.warp() == 6
    try:  # F
        o1.reset()
    except MealyError:
        pass
    assert o1.warp() == 9
    o1.reset()
    o1.color()
    o1.warp()
    o1.warp()
    o1.warp()
    assert o1.color() == 8
    try:  # G
        o1.color()
    except MealyError:
        pass
    assert o1.reset() == 11
    assert o1.warp() == 10
    try:  # H
        o1.color()
    except MealyError:
        pass
    try:  # H
        o1.warp()
    except MealyError:
        pass
    try:  # H
        o1.reset()
    except MealyError:
        pass
    test2()


def test2():
    o1 = main()
    o1.reset()
    o1.color()
    o1.warp()
    assert o1.reset() == 5
    o2 = main()
    o2.reset()
    o2.color()
    o2.warp()
    assert o2.color() == 4
