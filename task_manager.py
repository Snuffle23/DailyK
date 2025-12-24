import json
import datetime

def get_tasks(file):
    """Возвращает словарь с задачами
    file - путь к файлу с задачами"""

    #Проверить на существование 

    with open(file, "r", encoding="UTF-8") as to_do_list:
        tasks = json.load(to_do_list)
    return tasks

def create_task(tasks:dict={}): #реализовать множественное создание задач
    """Добавляет элемент(задачу) формата:
    "newTask":{"deadline":"dd-mm-yy","note":"description", "set":"dd-mm-yy"} 
    в указанный словарь
    task_list - указанный словарь""" 

    set = (datetime.date.today()).strftime("%d-%m-%y")
    task = input("task name: ")
    while task[-1] == " ":
        task = task[0:len(task)-1]
        
    if tasks.get(task, "") == "":#проверка на существование
        deadline = input("deadline - dd mm yy: ")#автоподстановка
        note = (s if (s:=input("note: ")) != "" else "")
        print(f"task \'{task}\' created.")
        tasks[task] = {"deadline":deadline, "note":note, "set":set}
    else:
        print(f"task \'{task}\' already exist.")

def upd_json(file, content:dict):
    """Записывает данные content в file(json)
    file - путь до файла
    content - запысываемые данные"""
    with open(file, 'w', encoding="UTF-8") as file_out:
        json.dump(content, file_out, ensure_ascii=False, indent=2)


