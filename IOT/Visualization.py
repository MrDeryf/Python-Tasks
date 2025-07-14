from matplotlib import pyplot as plt
import numpy as np
from json import load


def draw_hist(data: np.array):
    plt.xlabel("Значение движения")
    plt.ylabel("Частоты")
    plt.title("Движение")
    plt.grid(axis="y")
    plt.hist(data, bins=int(1 + np.log2(len(data))), edgecolor="black")
    plt.show()


def draw_line(data: np.array):
    plt.xlabel("Время")
    plt.ylabel("Значение CO2")
    plt.title("CO2")
    plt.grid(axis="y")
    plt.plot(data)
    plt.show()


def draw_pie(data: np.array):
    hist, edges = np.histogram(data)
    plt.title("Влажность")
    plt.pie(hist)
    plt.legend(labels=[f"[{edges[i]: .2f}, {edges[i+1]: .2f}]" for i in range(len(edges) - 1)], loc=4, draggable=True)
    plt.show()


def main():
    data1 = []
    data2 = []
    data3 = []
    with open("data.json") as f:
        data = load(f)
    for d in data:
        data1.append(int(d['motion']))
        data2.append(int(d['CO2']))
        data3.append(float(d['humidity']))
    print(data1, data2, data3)
    draw_hist(data1)
    draw_line(data2)
    draw_pie(data3)


if __name__ == "__main__":
    main()
