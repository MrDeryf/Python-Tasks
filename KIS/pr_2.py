from math import exp


def main(x):
    return (
        88 * x**6 - 22 * exp(x) ** 2
        if x < -26
        else 67 - 27 * x**3 - (25 * x**2 + 90 * x**3) ** 6 - 66
        if -26 <= x < 9
        else 49 * x - 28 * x**7 - 1
        if 9 <= x < 67
        else 89 - 58 * (41 - x**3) ** 5
    )


print(main(29))
