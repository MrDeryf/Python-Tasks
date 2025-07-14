from math import ceil, tan


def main(x, z):
    n = len(x)
    x = [0] + x
    z = [0] + z
    out = 0
    for i in range(1, n + 1):
        a = 99*(x[ceil(i/3)])**3 - x[i] - 25*(z[ceil(i/4)])**2
        out += 3 * tan(a) ** 3
    return 41 * out


print(main([0.92, 0.05, 0.04, -0.25, 0.92, 0.05],
[-0.56, 0.45, 0.05, -0.4, -0.31, -0.13]))
