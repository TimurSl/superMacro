import os
from typing import Dict

import main


def decrypt(file: str) -> list:
    """Decrypts a file and returns a dictionary with the keys and values."""
    # Проверяем, существует ли файл.
    if not os.path.exists(file):
        print("Файл не найден: " + file)
        exit(1)

    with open(file, 'r') as f:
        macro = [i.split() for i in f.read().splitlines()]

        # Проверяем, что в файле есть хотя бы одна команда.
        if len(macro) == 0:
            print("Файл пустой: " + file)
            exit(1)

        # Проверяем, что первая команда - это hotkey.
        if macro[0][0] != "hotkey":
            print("В файле нет hotkey: " + file)
            exit(1)

        # Проверяем, что вторая команда - это команда.
        if macro[1][0] not in ["click", "press", "release", "type", "delay"]:
            print("В файле нет команды: " + file)
            exit(1)

        # Проходимся по всем командам и проверяем, что они корректны.
        for i in macro:
            if i[0] == "hotkey":
                if len(i) != 2:
                    print("Неверное количество аргументов в hotkey: " + file)
                    exit(1)
            elif i[0] == "click":
                if len(i) != 2:
                    print("Неверное количество аргументов в click: " + file)
                    exit(1)
            elif i[0] == "press":
                if len(i) != 2:
                    print("Неверное количество аргументов в press: " + file)
                    exit(1)
            elif i[0] == "release":
                if len(i) != 2:
                    print("Неверное количество аргументов в release: " + file)
                    exit(1)
            elif i[0] == "type":
                if len(i) < 3:
                    print("Неверное количество аргументов в type: " + file)
                    exit(1)
                else:
                    # Объединяем все аргументы в одну строку.
                    # i[2] = " ".join(i[2:])
                    # del i[2:]
                    # Достаем второй аргумент и объединяем все остальные аргументы в одну строку.
                    i[2] = " ".join(i[2:])
                    del i[3:]

            elif i[0] == "delay":
                if len(i) != 2:
                    print("Неверное количество аргументов в delay: " + file)
                    exit(1)
            else:
                print("Неверная команда: " + file)
                exit(1)

        # Возвращаем список списков.
        return macro


        # data = f.read()
        # data = data.split('\n')
        # data = [i.split(' ') for i in data]
        # return data


