tree = {
    "NL": {
        "TWIG": {
            1978: {
                1984: 0,
                1975: 1,
                1996: 2,
            },
            1982: {
                "ABAP": 3,
                "VHDL": 4
            }
        },
        "JAVA": 5
    },
    "PIC": {
        1984: 6,
        1975: {
            1978: 7,
            1982: 8
        },
        1996: 9
    }
}

c = {
    "NL": 3,
    "PIC": 2,
    1975: 1,
    "TWIG": 1,
    1978: 2,
    1982: 0
}


def main(x):
    return main1(x, tree, 4)


def main1(x, _map, command_number):
    command = x[command_number]
    if type(_map[command]) == dict:
        _map = _map[command]
        return main1(x, _map, c[command])
    elif type(_map[command]) == int:
        return _map[command]
    else:
        raise Exception


print(main(['VHDL', 1982, 1996, 'JAVA', 'NL']))
