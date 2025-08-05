def main(line):
    splitted = line.split("<|")
    out = dict()
    for i in range(1, len(splitted)):
        first, second = splitted[i - 1 : i + 1]
        a = first[first.rfind("store") + 6 :].strip()
        b = second[: second.find(".")].strip()
        out[a] = b
    return out


print(main("{{ { store learima_749 <|lais. }, {store isin_877 <| riusla. }, }}"))
