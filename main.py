# -*- coding: utf-8 -*-
"""
GNU General Public License v3.0

Copyright (C) 2020-2021 by @zenisoft

This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
"""
import argparse
import sys
import time

import keyboard
import mouse as m
from art import tprint, text2art
from past.builtins import raw_input

import commands
import file_decryptor

import colorama as color
import readline

color.init()

file = None
macro_dict = None
debug = False

script_run_times = 0

current_version = "1.2.0"

script_completed_position = None

can_cmd = False

mouse_buttons = [
    ["ЛКМ", "lmb", m.LEFT],
    ["ПКМ", "rmb", m.RIGHT],
    ["СКМ", "mmb", m.MIDDLE],
    ["Кнопка 4", "x1", m.X],
    ["Кнопка 5", "x2", m.X2]
]


def main():
    global file, macro_dict, debug
    welcome()
    readline.parse_and_bind("tab: complete")
    parser = argparse.ArgumentParser()
    parser.add_argument("-script", help="Запустить макрос из файла")
    # Добавить аргумент для отладки, если он есть, то включить отладку
    parser.add_argument("-debug", help="Включить отладку", action="store_true")
    args = parser.parse_args()
    if args.script:
        file = args.script
    else:
        file = raw_input("Введите путь к макросу: ")

    if args.debug:
        debug = True
        print("Отладка включена")

    macro_dict = file_decryptor.decrypt(file)
    if debug:
        print(macro_dict)
    print("Макрос загружен: " + file)

    hotkey = get_hotkey()
    if hotkey in mouse_buttons:
        pass
    else:
        keyboard.add_hotkey(hotkey, run_macro)
    print("Нажмите " + color.Fore.RED + hotkey + color.Fore.RESET + " для запуска макроса")
    clearhotkey = get_clear_hotkey()
    if clearhotkey != None:
        keyboard.add_hotkey(clearhotkey, clear_script_run_times)
        print("Нажмите " + color.Fore.RED + clearhotkey + color.Fore.RESET + " для очистки количества запусков макроса")

def clear_script_run_times():
    global script_run_times
    script_run_times = 0
    sys.stdout.write(
        f"Количество выполнений макроса {color.Fore.LIGHTGREEN_EX}успешно{color.Style.RESET_ALL} сброшено\r"
    )
    sys.stdout.flush()

def run_macro():
    global macro_dict, script_run_times
    if macro_dict is not None:
        """
        Проходимся по всему словарю и выполняем команды.
        """
        for i in macro_dict:
            command = i[0]
            first_arg = i[1]
            if debug:
                print(f"Команда: {command}, Аргумент: {first_arg}")
            # click - нажать кнопку
            if command == "click":
                # Проверка, являеться ли клавиша кнопкой мыши
                if is_mouse_button(first_arg):
                    # Нажатие клавиши
                    commands.mouse_click(get_button_by_code(first_arg)[2])
                    # Если включен режим отладки
                    if debug:
                        # Вывести сообщение
                        print("Клик кнопки " + get_button_by_code(first_arg)[0])
                # Если не являеться
                else:
                    # Нажатие клавиши
                    commands.click(first_arg)
                    # Если включен режим отладки
                    if debug:
                        # Вывести сообщение
                        print("Клик клавиши " + first_arg)
            elif command == "press":
                if is_mouse_button(first_arg):
                    commands.mouse_press(get_button_by_code(first_arg)[2])
                    if debug:
                        print("Нажатие кнопки " + get_button_by_code(first_arg)[0])
                else:
                    commands.click(first_arg)
                    if debug:
                        print("Нажатие клавиши " + first_arg)
            elif command == "release":
                if is_mouse_button(first_arg):
                    commands.mouse_click(get_button_by_code(first_arg)[2])
                    if debug:
                        print("Отпускание кнопки " + get_button_by_code(first_arg)[0])
                else:
                    commands.click(first_arg)
                    if debug:
                        print("Отпускание клавиши " + first_arg)
            elif command == "type":
                interval = int(i[1]) / 1000
                text = i[2]
                if debug:
                    print("Печать текста " + text + " с интервалом " + str(interval))
                commands.type(text, interval)
            elif command == "delay":
                time.sleep(float(first_arg) / 1000)
                if debug:
                    print("Задержка " + first_arg + " миллисекунд")
            elif command == "moveto":
                x = int(i[1])
                y = int(i[2])
                # Проверить, есть ли 3 аргумент
                if len(i) == 4:
                    # Если есть, то присвоить его переменной
                    duration = int(i[3]) / 1000
                else:
                    # Если нет, то присвоить 0.1
                    duration = 0.1
                if debug:
                    print("Перемещение курсора на " + str(x) + " " + str(y))
                commands.mouse_move_to(x, y, duration)
            elif command == "move":
                x = int(i[1])
                y = int(i[2])
                if len(i) == 4:
                    duration = int(i[3]) / 1000
                else:
                    duration = 0.1
                if debug:
                    print("Перемещение курсора на " + str(x) + " " + str(y))
                commands.mouse_move(x, y, duration)

            else:
                print(f"Команда {command} не найдена")

        script_run_times += 1

        script_completed()


def script_completed():
    # Очистить строку
    print(" " * 100, end="\r")
    sys.stdout.write(
        f"Макрос выполнен {color.Fore.CYAN + color.Style.BRIGHT}(x{str(script_run_times)}){color.Style.RESET_ALL}\r"
    )
    sys.stdout.flush()


def get_hotkey() -> str:
    """Получить первый элемент из словаря макроса."""
    global macro_dict
    if macro_dict is not None:
        # Получить значение первого элемента словаря
        hotkey = macro_dict[0][1]
        del macro_dict[0]
        return hotkey
    else:
        print("Файл не найден")

def get_clear_hotkey() -> str:
    """
    Найти елемент в котором есть команда resetkey
    """
    for i in macro_dict:
        if i[0] == "resetkey":
            resetkey = i[1]
            macro_dict.remove(i)
            return i[1]

def welcome():
    art = text2art("MACRO", font="block", chr_ignore=True)
    msg = color.Fore.MAGENTA + art
    print(msg)
    style = color.Style.BRIGHT + color.Fore.CYAN
    reset = color.Style.RESET_ALL
    print(color.Fore.RESET + "Автор: " + style + "Zenisoft" + reset)
    print(color.Fore.RESET + "Версия: " + style + current_version + reset)
    print(color.Fore.RED + "Welcome to Macro Player" + color.Fore.RESET)
    print("Нажмите " + color.Fore.RED + "Ctrl + C" + color.Fore.RESET + " для выхода")


def delete_last_line():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')


def is_mouse_button(button: str) -> bool:
    for b in mouse_buttons:
        if debug:
            print(f"Код: {b[1]}, аргумент: {button}, совпадают: {b[1] == button}")
        if b[1] == button:
            return True
        else:
            continue


def get_button_by_code(code: str):
    for b in mouse_buttons:
        if debug:
            print(f"Код: {b[1]}, аргумент: {code}, совпадают: {b[1] == code}")
        if b[1] == code:
            return b
        else:
            continue


if __name__ == '__main__':
    main()
    keyboard.wait()
