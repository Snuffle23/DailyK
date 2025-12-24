import json
import datetime

def name_normalize(name):
    while name != "":#Генерация и проверка имени
        if name.startswith(" ") or name.endswith(" "):
            while name.endswith(" "):
                name = name[0:-2]
            while name.startswith(" "):
                name = name[1::]
        break
    return name

def get_json(file):
    """Возвращает словарь с задачами
    file - путь к файлу с задачами"""

    with open(file, "r", encoding="UTF-8") as file_in:
        result = json.load(file_in)
    return result

def create_task(tasks:dict={}): #реализовать множественное создание задач
    """Добавляет задачу в указанный словарь
    tasks - указанный словарь""" 
    name = name_normalize(input("Название: "))
    while not (name not in tasks.keys()) and (name != ""):
        name = name_normalize(input("Попробуйте другое: "))
    if not name:
        return
    #Генерация контента
    set = (datetime.date.today()).strftime("%d-%m-%y")
    deadline = input("Дедлайн: ")
    note = input("Описание: ")
    difficult = {1:"easy", 2:"midl", 3:"hard", 4:"complex"}[int(input("Сложность 1-4: "))]# Обработка оштбок
    if difficult == "complex":
        components = {}
        while (subtask := input("Подзадача: ")) != "":
            subtask = name_normalize(subtask)
            while subtask in components.keys() and (subtask != ""):
                subtask = name_normalize(input("Попробуйте другое: "))
            sub_difficult = {1:"easy", 2:"midl", 3:"hard"}[int(input("Сложность 1-3: "))]
            components[subtask] = {"note": input("Описание: "), "difficult":sub_difficult, "complete":0}
        tasks[name] = {"deadline": deadline,
                        "note": note,
                        "difficult": difficult,
                        "components":components,
                        "set": set, "complete": 0}
        return
    tasks[name] = {"deadline": deadline,
                        "note": note,
                        "difficult": difficult,
                        "set": set, "complete": 0}
    return

def upd_json(file, content:dict):
    """Записывает данные content в file(json)
    file - путь до файла
    content - запысываемые данные"""
    with open(file, 'w', encoding="UTF-8") as file_out:
        json.dump(content, file_out, ensure_ascii=False, indent=2)


