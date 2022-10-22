"""
Команды, доступные в программе
click - нажимает и отпускает клавишу
press - нажимает клавишу и удерживает её
release - отпускает клавишу
type - печатает текст
"""
import keyboard
import mouse
import time


# Команда click
def click(key):
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)


# Команда press
def press(key):
    keyboard.press(key)


# Команда release
def release(key):
    keyboard.release(key)


# Команда type
def type(text, interval):
    # Обьединяем аргументы в одну строку
    keyboard.write(text, delay=interval)


def mouse_click(button):
    mouse.click(button=button)


def mouse_press(button):
    mouse.press(button)


def mouse_release(button):
    mouse.release(button)


def mouse_move_to(x, y, duration=0.1):
    mouse.move(x, y, duration=duration)


def mouse_move(x, y, duration=0.1):
    mouse.move(x, y, absolute=False, duration=duration)
