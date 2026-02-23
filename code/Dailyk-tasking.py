from task_manager import *
from testing import *
import json, datetime

filter_rules = """
<1 не выполненные
>0 начатые
==0 не начатые
==1 выполненные
>0.33 Выполненные больше чем на 0.33
<0.66 Выполненные меньше чем на 0.66
==0.5 Выполненные строго на половину"""
def init():
    print(nav_bar)
    while not (choise := input("Действие: ")).isdigit():
        continue
    return int(choise)

print("Welcome to Dailyk Pre-alpha\n"+"---"*15)
nav_bar = "[1] - Добавить задачу\n[2] - Список всех задач"

while (choise:=init()) != "":
    if choise == 1:
        add_task()
    if choise == 2:
        if input("Если оставить это поле пустым, появятся только невыполненные задачи. Хотите поменять шаблон фильтра?: "):
            f = ff if (ff := input("Фильтр('complete(по умолчанию)' 'deadline' 'difficult'  'estime'): ")) else "complete"
            if f == "complete":
                print(filter_rules)
            rule = input("Правило(< > == != <= >=): ")
            mark = input("Аргумент(0 0.5 1 дд.мм.гггг): ")
            print(task_filter(f, rule, mark))
        else:
            print(task_filter())

