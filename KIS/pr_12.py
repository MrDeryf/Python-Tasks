from struct import unpack


def main1(a, index, data):
    a["A5"] = []
    size = unpack(">L", data[index:index + 4])[0]
    index += 4
    address = unpack(">L", data[index:index + 4])[0]
    index += 4
    for _ in range(size):
        a["A5"].append(dict())
        d = a["A5"][-1]
        address1 = unpack(">L", data[address:address + 4])[0]
        address += 4
        d["D1"] = unpack(">h", data[address1:address1 + 2])[0]
        address1 += 2
        d["D2"] = []
        size1 = unpack(">H", data[address1:address1 + 2])[0]
        address1 += 2
        address2 = unpack(">L", data[address1:address1 + 4])[0]
        address1 += 4
        for _ in range(size1):
            d["D2"].append(unpack(">f", data[address2:address2 + 4])[0])
            address2 += 4
    return index


def main(data):
    a = dict()
    index = 3

    a["A1"] = unpack(">f", data[index:index + 4])[0]
    index += 4

    a["A2"] = unpack(">H", data[index:index + 2])[0]
    index += 2

    a["A3"] = unpack(">H", data[index:index + 2])[0]
    index += 2

    a["A4"] = dict()
    b = a["A4"]
    b["B1"] = dict()
    c = b["B1"]
    address = unpack(">L", data[index:index + 4])[0]
    index += 4
    c["C1"] = unpack(">L", data[address:address + 4])[0]
    address += 4
    c["C2"] = unpack(">h", data[address:address + 2])[0]
    address += 2
    c["C3"] = unpack(">B", data[address:address + 1])[0]
    address += 1
    c["C4"] = unpack(">b", data[address:address + 1])[0]
    address += 1
    b["B2"] = unpack(">Q", data[index:index + 8])[0]
    index += 8
    b["B3"] = ""
    size = unpack(">H", data[index:index + 2])[0]
    index += 2
    address = unpack(">H", data[index:index + 2])[0]
    index += 2
    for _ in range(size):
        b["B3"] += chr(unpack(">B", data[address:address+1])[0])
        address += 1
    b["B4"] = unpack(">b", data[index:index+1])[0]
    index += 1
    b["B5"] = ""
    for _ in range(3):
        b["B5"] += chr(unpack(">B", data[index:index+1])[0])
        index += 1
    index = main1(a, index, data)
    a["A6"] = []
    size = unpack(">L", data[index:index + 4])[0]
    index += 4
    address = unpack(">L", data[index:index + 4])[0]
    index += 4
    for _ in range(size):
        a["A6"].append(unpack(">f", data[address:address + 4])[0])
        address += 4
    return a

data_1 = (b'DMX\xbf\x14\x1e\x01\xab2;Y\x00\x00\x00/\xb8\x0cU9\x19\xa9\xe1\x0b\x00'
 b'\x02\x007Fahs\x00\x00\x00\x02\x00\x00\x00Y\x00\x00\x00\x04\x00\x00\x00a\xa6'
 b'#u\xfcRI\xdf\xfcqy\xbe\xa4D^\xbe9K\x96T^\x00\x02\x00\x00\x009?R:_>\xb3\xb3'
 b'\xebv\x96\x00\x02\x00\x00\x00I\x00\x00\x00A\x00\x00\x00Q?+\xa3\xbf=Y8\xb7?x?'
 b'\xec\xbe\xbf\xe48')

print(main(data_1))
