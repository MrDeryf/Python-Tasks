def main(table):
    new_table = []
    for line in table:
        if line[0] is not None:
            a = line[4][-4:-2]+" "+line[4][:line[4].find(",")]
            b, c, d = line[5].split("-")
            new_line = [line[0][7:13] + "-" + line[0][13:],
                        line[1][line[1].find("]") + 1:],
                        a,
                        ".".join([d, c, b])
                        ]
            if new_line not in new_table:
                new_table.append(new_line)
    return sorted(new_table, key=lambda x: x[2])

x = [[' 737-81-62', 'mail.ru', 'А. Шолук', '00.10.19'],
     [' 869-64-83', 'rambler.ru', 'В. Зедекиди', '03.12.17'],
     [' 299-19-33', 'mail.ru', 'В. Тоцигян', '00.09.02'],
     [' 067-99-90', 'rambler.ru', 'М. Фуцасук', '00.03.13']]
print(main([[None, 'Родли Д.Ш.:нет', None, '0.6', 'rodli82@gmail.com'], [None, 'Филерянц Г.Л.:нет', None, '0.4', 'fileranz58@mail.ru'], [None, 'Сишич В.С.:да', None, '0.1', 'sisic59@mail.ru']]))