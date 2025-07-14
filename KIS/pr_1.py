import math


def main(y, x):
    return ((86 * x ** 3 + x + y ** 2 / 68) ** 6 + 95 * math.log10(1 - 61 * x ** 3) ** 4) / (96 * y ** 5 + 43 * x ** 7) + (y ** 7 - x ** 6) ** 0.5


print(main(0.61, 0.17))

