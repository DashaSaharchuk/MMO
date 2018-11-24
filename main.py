import random
import math
import csv

distances = []

def get_distances_train(train_data):
    distances.clear()
    length = len(train_data)
    point_distance = []
    for i in range(length):
        for j in range(length):
            point_distance.append([dist(train_data[i], train_data[j]), train_data[j][2]])
        distances.append(point_distance.copy())
        point_distance.clear()
        distances[i].sort(key=lambda e: e[0])

def get_distances_test(train_data, test_data):
    distances.clear()
    point_distance = []
    test_length = len(test_data)
    train_length = len(train_data)
    for i in range(test_length):
        for j in range(train_length):
            point_distance.append([dist(test_data[i], train_data[j]), train_data[j][2]])
        distances.append(point_distance.copy())
        point_distance.clear()
        distances[i].sort(key=lambda e: e[0])

def dist(a, b):
    return math.sqrt((a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]))

def get_k(train_data):
    minimum = 100000
    answer = 0
    for k in range(3, 50, 2):
        neigh = LOO(train_data, k)
        if neigh < minimum:
            minimum = neigh
            answer = k
    return answer

def LOO(train_data, k):
    summa = 0
    length = len(train_data)
    for i in range(length):
        summa += int(parsen(i, k) != train_data[i][2])
    return summa

def kernel(y):
    return ((1 - abs(y) * abs(y)) * (1 - abs(y) * abs(y))) * int(abs(y) <= 1)

def parsen(index_u, k):
    maximum = 0
    answer = 0
    for y in range(2):
        neigh_k = distances[index_u][k + 1]
        summa = 0
        for i in range(1, k + 1):
            neigh_i = distances[index_u][i]
            summa += int(neigh_i[1] == y) * kernel(neigh_i[0] / neigh_k[0])
        if summa > maximum:
            maximum = summa
            answer = y
    return answer

def split_on_test_and_train(data, percent_test):
    train_data = []
    test_data = []
    for i in range(len(data)):
        random_number = random.randint(0, len(data) - 1)
        if random.random() < percent_test:
            test_data.append(data[random_number])
            data.remove(data[random_number])
        else:
            train_data.append(data[random_number])
            data.remove(data[random_number])
    return train_data, test_data

def read_file():
    data = []
    csv_file = open('E:/Programs/Python/data5.csv')
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        else:
            data.append([int(row[0]), int(row[1]), int(row[2])])
    return data

def count_of_objects(list, object_class):
    count = 0
    for i in range(len(list)):
        if list[i][2] == object_class:
            count += 1
    return count

def main():
    data = read_file()
    count = count_of_objects(data, 0)
    print('Количество объектов класса 0 в исходной выборке:', count, '(',
          (count * 100) / len(data), '% )')
    count = count_of_objects(data, 1)
    print('Количество объектов класса 1 в исходной выборке:', count, '(',
          (count * 100) / len(data), '% )\n')
    for i in range(10):
        data = read_file()
        print('Разбиение', i + 1, '\n')
        train, test = split_on_test_and_train(data, 0.4)
        count = count_of_objects(train, 0)
        print('Количество объектов класса 0 в обучающей выборке:', count, '(',
              (count * 100) / len(train), '% )')
        count = count_of_objects(train, 1)
        print('Количество объектов класса 1 в обучающей выборке:', count, '(',
              (count * 100) / len(train), '% )')
        count = count_of_objects(test, 0)
        print('Количество объектов класса 0 в тестовой выборке:', count, '(',
              (count * 100) / len(test), '% )')
        count = count_of_objects(test, 1)
        print('Количество объектов класса 1 в тестовой выборке:', count, '(',
              (count * 100) / len(test), '% )')
        get_distances_train(train)
        k = get_k(train)
        print('\nКоличество соседей k =', k)
        get_distances_test(train, test)
        mistakes = 0
        for val in test:
            answer = parsen(test.index(val), k)
            mistakes += int(answer != val[2])
        print('Количество ошибок на тестовой выборке:', mistakes, '(', (mistakes * 100) / len(test), '% )\n')

if __name__ == "__main__":
    main()
