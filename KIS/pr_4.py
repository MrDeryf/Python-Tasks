from math import log, exp


def main(n):
    if n == 0:
        return -0.79
    if n == 1:
        return -1.00
    return (1 - main(n-1) / 68) ** 2 - 11 * main(n-2)


print(main(5))
