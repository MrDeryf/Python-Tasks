def main(n, b):
    if b == 1:
        return my_rec(n, b)
    return my_rec(n, b) + main(n, b - 1)


def my_rec(n, b):
    if n == 1:
        return (47 * n
                - (abs(13 * n**2 - 70) ** 7) / 32
                - (81 * b**3 + 1 + n) ** 2
                )
    return (
        my_rec(n - 1, b)
        + 47 * n
        - (abs(13 * n**2 - 70) ** 7) / 32
        - (81 * b**3 + 1 + n) ** 2
    )


print(main(5, 7))
