def main(number):
    data = number
    fields = [
        ('V1', 8),
        ('V2', 8),
        ('V3', 9),
        ('V4', 9),
        ('V5', 1),
        ("V6", 3)
    ]
    decomposition = dict()
    for name, size in fields:
        value = data & ((1 << size) - 1)
        decomposition[name] = value
        data >>= size
    decomposition["V3"] = 0
    new_order = [
        ('V2', 8),
        ('V3', 9),
        ('V5', 1),
        ('V4', 9),
        ('V1', 8)
    ]
    out = decomposition["V6"]
    for name, size in new_order:
        out <<= size
        out += decomposition[name]

    return out


print(main(84055023173))
