from task_manager import *
from testing import *
import json, datetime

def init():
    print(nav_bar)
    choise = input("Действие:")
    while not (choise := input("Действие: ")).isdigit():
        continue
    return choise

print("Welcome to Dailyk Pre-alpha\n"+"---"*15)
nav_bar = "[1] - Добавить задачу\n[2] - Список всех задач"
choise = 1
while choise != "":
    choise = init()

    choise = int(choise)
    if choise == 1:
        add_task()
    if choise == 2:
        if input("Использовать ли фильтрацию?\n(Оставьте пустым если не нужно) -у: "):
            f = input("Аргумент: ")
            rule = input("Правило: ")
            mark = input("Направление: ")
            print(task_filter(f, rule, mark))
        else:
            print(task_filter())