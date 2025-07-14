import numpy as np
from matplotlib import pyplot as plt


def avr(array: np.array):
    return round(sum(array) / len(array), 2)


def disp(array: np.array):
    return round(sum((array - avr(array)) ** 2) / len(array), 2)


def st_dev(array: np.array):
    return round(np.sqrt(disp(array)), 2)


def median(array: np.array):
    mid = len(array) // 2
    return array[mid] if len(array) % 2 == 1 else round(sum(array[mid-1:mid]) / 2, 2)


def variation(array: np.array):
    return round(st_dev(array) / avr(array), 2)


data = {"Рост": [1.80, 1.62, 1.65, 1.82, 1.68, 1.64, 1.76, 1.65, 1.92],
        "Месяц": [4, 1, 8, 4, 12, 11, 3, 10, 1],
        "Число": [3, 7, 2, 0, 2, 7, 4, 0, 1]}

month = np.sort(data["Месяц"])
number = np.sort(data["Число"])
height = np.sort(data["Рост"])


m = round(1 + np.log2(len(height)))
h = (height[-1] - height[0]) / m


intervals = np.round(np.arange(height[0] - h / 2, height[-1] + h / 2, h), 4)

freq = []
i = 1
count = 0
for el in height:
    if el < intervals[i]:
        count += 1
    else:
        freq.append(count)
        count = 1
        i += 1
freq.append(count)
freq = np.array(freq)

r_freq = np.round(freq / len(height), 2)

print(intervals[:-1])
print(intervals[1:])
print(freq)
print(r_freq)
arr = []
for i in range(len(intervals) - 1):
    arr += ([round(sum(intervals[i:i+2]) / 2, 2)] * freq[i])

cumul_sum = 0
index = 0
prev_sum = 0
for i in range(len(r_freq)):
    prev_sum = cumul_sum
    cumul_sum += r_freq[i]
    if cumul_sum > 0.5:
        index = i
        break
prev_sum *= len(arr)
med = intervals[index] + ((0.5 * len(arr) - prev_sum) / freq[i]) * h
print(med)
