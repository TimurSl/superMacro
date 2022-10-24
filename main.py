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
import mouse
import mouse as m
from art import tprint, text2art
from past.builtins import raw_input

import commands
import file_decryptor

import colorama as color
import readline
import win32gui, win32process, os

color.init()

file = None
macro_dict = None
debug = False

script_run_times = 0
current_version = "1.3.2"

reset_macro_type = 'back'
hotkey = None
mouse_buttons = [
    ["ЛКМ", "lmb", m.LEFT],
    ["ПКМ", "rmb", m.RIGHT],
    ["СКМ", "mmb", m.MIDDLE],
    ["Кнопка 4", "x1", m.X],
    ["Кнопка 5", "x2", m.X2]
]


def main():
    global file, macro_dict, debug, reset_macro_type, hotkey
    welcome()
    readline.parse_and_bind("tab: complete")

    parser = argparse.ArgumentParser()

    parser.add_argument("-script", help="Запустить макрос из файла")
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
    print("Загрузка макроса...")
    if debug:
        print(macro_dict)

    hotkey = get_hotkey()
    if debug:
        print("Горячая клавиша: " + str(hotkey))

    if is_mouse_button(hotkey):
        # Привязываем обработчик событий мыши
        mouse.hook(mouse_handler)
    else:
        keyboard.add_hotkey(hotkey, run_macro)

    if not is_mouse_button(hotkey):
        print("Нажмите " + color.Fore.RED + hotkey + color.Fore.RESET + " для запуска макроса")
    else:
        name = get_name_by_button(hotkey)
        if debug:
            print("Название кнопки: " + name)
        print("Нажмите " + color.Fore.RED + name + color.Fore.RESET + " для запуска макроса")

    listClear = get_clear_hotkey()
    clearhotkey = listClear[0]
    reset_macro_type = listClear[1]

    if clearhotkey != None:
        keyboard.add_hotkey(clearhotkey, clear_script_run_times)
        print("Нажмите " + color.Fore.RED + clearhotkey + color.Fore.RESET + " для очистки количества запусков макроса")

    print("Макрос загружен: " + file)



def mouse_handler(event):
    # Если событие это ButtonEvent
    if isinstance(event, mouse.ButtonEvent):
        if debug:
            print("Нажата кнопка мыши: " + str(event.button) + " А хоткей: " + str(hotkey) + " А переведенный хоткей: " + str(get_button_by_code(hotkey)[2]))
        # Если нажата кнопка мыши, которая указана в макросе
        if event.button == get_button_by_code(hotkey)[2]:
            # Если нажата кнопка мыши, которая указана в макросе
            if event.event_type == mouse.UP:
                # Запустить макрос
                run_macro()

    # down - вызывается при нажатии кнопки мыши
    # up - вызывается при отпускании кнопки мыши
    # wheel - вызывается при прокрутке колеса мыши
    # move - вызывается при перемещении мыши
    # scroll - вызывается при прокрутке колеса мыши
    # double - вызывается при двойном нажатии кнопки мыши
    # triple - вызывается при тройном нажатии кнопки мыши
    # quadruple - вызывается при четырехкратном нажатии кнопки мыши
    # button - вызывается при нажатии кнопки мыши
    # drag - вызывается при перемещении мыши с зажатой кнопкой мыши
    # drop - вызывается при отпускании кнопки мыши после перемещения мыши с зажатой кнопкой мыши
    # enter - вызывается при наведении мыши на объект
    # leave - вызывается при уходе мыши с объекта
    # click - вызывается при нажатии и отпускании кнопки мыши
    # press - вызывается при нажатии кнопки мыши
    # release - вызывается при отпускании кнопки мыши



def clear_script_run_times():
    global script_run_times
    focus_window_pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())[1]
    current_process_pid = os.getppid()

    if focus_window_pid == current_process_pid:
        if reset_macro_type == "fore":
            script_run_times = 0
            sys.stdout.write(
                f"Количество выполнений макроса {color.Fore.LIGHTGREEN_EX}успешно{color.Style.RESET_ALL} сброшено\r"
            )
            sys.stdout.flush()
        elif reset_macro_type == "back":
            script_run_times = 0
            sys.stdout.write(
                f"Количество выполнений макроса {color.Fore.LIGHTGREEN_EX}успешно{color.Style.RESET_ALL} сброшено\r"
            )
            sys.stdout.flush()
    else:
        if reset_macro_type == "back":
            script_run_times = 0
            sys.stdout.write(
                f"Количество выполнений макроса {color.Fore.LIGHTGREEN_EX}успешно{color.Style.RESET_ALL} сброшено\r"
            )
            sys.stdout.flush()
        elif reset_macro_type == "fore":
            pass


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
                # Проверка, является ли клавиша кнопкой мыши
                if is_mouse_button(first_arg):
                    # Нажатие клавиши
                    commands.mouse_click(get_button_by_code(first_arg)[2])
                    # Если включен режим отладки
                    if debug:
                        # Вывести сообщение
                        print("Клик кнопки " + get_button_by_code(first_arg)[0])
                # Если не является
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


def get_clear_hotkey() -> list:
    """
    Найти елемент в котором есть команда resetkey
    """
    for i in macro_dict:
        if i[0] == "resetkey":
            try:
                clear_type = i[2]
            except IndexError:
                clear_type = "back"
            resetkey = i[1]

            macro_dict.remove(i)
            clear_list = [resetkey, clear_type]
            return clear_list


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

def get_name_by_button(button: str):
    for b in mouse_buttons:
        if debug:
            print(f"Код: {b[1]}, аргумент: {button}, совпадают: {b[1] == button}")
        if b[1] == button:
            return b[0]
        else:
            continue


if __name__ == '__main__':
    main()
    keyboard.wait()
