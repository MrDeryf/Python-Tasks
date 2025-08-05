from math import ceil


def main(x: set):
    o = {6 * el for el in x if (el > -48) and (el < 79)}
    p = {el + 6 * el for el in o if (el < -44) or (el > 47)}
    f = x | o
    delta = {ceil(el / 4) - el for el in f if (el >= 89)}
    e = p | delta
    out = len(delta) + sum(e)
    return out


print(main({2, 99, 68, 73, -79, 51, -76, -73, 91, -2}))
