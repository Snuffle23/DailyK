import json, datetime #pyside6-designer
from task_manager import *

tasks = get_json("tasks")
def show_tasks():
    for i, task in enumerate(tasks):
        print(i+1, task)
        for arg in tasks[task].keys():
            if arg == "components":
                print(f"  components:")
                for sub_tusk in tasks[task][arg]:
                    print(f"  - {sub_tusk}")
                    for subArg in tasks[task][arg][sub_tusk]:
                        print(f"      {subArg} - {tasks[task][arg][sub_tusk][subArg]}")
            else:
                print(f"  {arg} - {tasks[task][arg]}")

def add_task():
    
    while (name := input("Имя задачи: ")) != "": 
        name = name_normalize(name, tasks)
        deadline = input("Дэдлайн: ")
        estime = int(input("Расчётное время: "))
        tasks[name] = tasking(estime, deadline)
        upd_json("tasks", tasks)

def dtools(choise:int=1):
    if choise == 1:
        show_tasks()
    elif choise == 2:
        add_task()

