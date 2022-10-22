# -*- coding: utf-8 -*-
"""
GNU General Public License v3.0

Copyright (C) 2020-2021 by @zenisoft

This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under certain conditions.
"""
import argparse
import distutils
import os
import subprocess
import time

import keyboard
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
        file = input("Введите путь к макросу: ")

    if args.debug:
        debug = True
        print("Отладка включена")

    macro_dict = file_decryptor.decrypt(file)
    if debug:
        print(macro_dict)
    print("Макрос загружен: " + file)

    hotkey = get_hotkey()
    keyboard.add_hotkey(hotkey, run_macro)
    print("Нажмите " + color.Fore.RED + hotkey + color.Fore.RESET + " для запуска макроса")


def run_macro():
    global macro_dict
    if macro_dict is not None:
        """
        Проходимся по всему словарю и выполняем команды.
        """
        for i in macro_dict:
            command = i[0]
            first_arg = i[1]

            if command == "click":
                if first_arg == "lmb":
                    commands.mouse_click("left")
                    if debug:
                        print("Клик левой кнопкой мыши")
                elif first_arg == "rmb":
                    commands.mouse_click("right")
                    if debug:
                        print("Клик правой кнопкой мыши")
                elif first_arg == "mmb":
                    commands.mouse_click("middle")
                    print("Клик средней кнопкой мыши")
                else:
                    commands.click(first_arg)
                    if debug:
                        print("Клик клавиши " + first_arg)
            elif command == "press":
                if first_arg == "lmb":
                    commands.mouse_press("left")
                    if debug:
                        print("Нажатие левой кнопкой мыши")
                elif first_arg == "rmb":
                    commands.mouse_press("right")
                    if debug:
                        print("Нажатие правой кнопкой мыши")
                elif first_arg == "mmb":
                    commands.mouse_press("middle")
                    if debug:
                        print("Нажатие средней кнопкой мыши")
                else:
                    commands.press(first_arg)
                    if debug:
                        print("Нажатие клавиши " + first_arg)
            elif command == "release":
                if first_arg == "lmb":
                    commands.mouse_release("left")
                    if debug:
                        print("Отпускание левой кнопкой мыши")
                elif first_arg == "rmb":
                    commands.mouse_release("right")
                    if debug:
                        print("Отпускание правой кнопкой мыши")
                elif first_arg == "mmb":
                    commands.mouse_release("middle")
                    if debug:
                        print("Отпускание средней кнопкой мыши")
                else:
                    commands.release(first_arg)
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
            else:
                print(f"Команда {command} не найдена")
        print("Макрос выполнен")


def get_hotkey() -> str:
    """Получить первый елемент из словаря макроса."""
    global macro_dict
    if macro_dict is not None:
        # Получить значение первого элемента словаря
        hotkey = macro_dict[0][1]
        del macro_dict[0]
        return hotkey
    else:
        print("Файл не найден")


def welcome():
    art = text2art("MACRO", font="block", chr_ignore=True)
    msg = color.Fore.MAGENTA + art
    print(msg)
    style = color.Style.BRIGHT + color.Fore.CYAN
    reset = color.Style.RESET_ALL
    print(color.Fore.RESET + "Автор: " + style + "Zenisoft" + reset)
    print(color.Fore.RESET + "Версия: " + style + "1.1.0" + reset)
    print(color.Fore.RED + "Welcome to Macro Player" + color.Fore.RESET)
    print("Нажмите " + color.Fore.RED + "Ctrl + C" + color.Fore.RESET + " для выхода")


if __name__ == '__main__':
    main()
    keyboard.wait()
