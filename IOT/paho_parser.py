from json import load
import xml.etree.ElementTree as ET


def parse_json(file_name):
    #Парсим JSON
    with open(file_name) as f:
        data = load(f)
    return data


def parse_xml(file_name):
    # Парсим XML
    tree = ET.parse(file_name)
    root = tree.getroot()
    out = []
    for data in root:
        out.append(dict())
        for info in data:
            out[-1][info.tag] = info.text
    return out


def main():
    print(parse_json("data.json"))
    print(parse_xml("data.xml"))


if __name__ == "__main__":
    main()
