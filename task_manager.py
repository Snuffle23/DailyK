import json
import datetime


def get_json(file):
    """Возвращает словарь с задачами
    file - путь к файлу с задачами"""

    with open(file, "r", encoding="UTF-8") as file_in:
        result = json.load(file_in)
    return result

def upd_json(file, content:dict):
    """Записывает данные content в file(json)
    file - путь до файла
    content - запысываемые данные"""
    with open(file, 'w', encoding="UTF-8") as file_out:
        json.dump(content, file_out, ensure_ascii=False, indent=4)


def name_normalize(name:str=""):
    """Возвращает нормализированную строку (без пробелов в начале и в конце)"""
    while name != "":#Генерация и проверка имени
        if name.startswith(" ") or name.endswith(" "):
            while name.endswith(" "):
                name = name[0:-2]
            while name.startswith(" "):
                name = name[1::]
        break
    return name

def flag_filter(tasks:dict, complete=0):
    """Возвращает список кортежей формата (Имя, флаг выполнения, '{компоненты}если есть')
    tasks - словарь с задачами
    complete - флаг возвращаемых задач"""
    result = []
    for task in tasks: # имя задачи
        intermediate = dict()
        if tasks[task].get("components", False):
            counter = 0
            for subtask in tasks[task]["components"]:
                subflag = tasks[task]["components"][subtask]["complete"]
                if complete == 0 and subflag < 1:
                    intermediate[subtask] = subflag
                elif complete == 1 and subflag == 1:
                    intermediate[subtask] = subflag
                counter += subflag

        flag = tasks[task]["complete"] # флаг выполнения
        if complete == 0 and flag < 1:
            result.append((task, float(f'{counter / len(tasks[task]["components"].keys()):.2f}'), {"components":intermediate}) if intermediate else (task, flag))
        elif complete == 1 and flag == 1:
            result.append((task))
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
    difficult = {1:"easy", 2:"midl", 3:"hard", 4:"complex"}[int(num)] if ((num:=input("Сложность 1-4: ")) < "5") and num.isdigit() else 1
    if difficult == "complex":
        components = {}
        while (subtask := input("Подзадача: ")) != "":
            subtask = name_normalize(subtask)
            while subtask in components.keys() and (subtask != ""):
                subtask = name_normalize(input("Попробуйте другое: "))
            sub_difficult = {1:"easy", 2:"midl", 3:"hard"}[int(num)] if ((num:=input("Сложность 1-3: ")) < "4") and num.isdigit() else 1
            components[subtask] = {"note": input("Описание: "), "difficult":sub_difficult, "complete":0}
        tasks[name] = {
            "deadline": deadline,
            "note": note,
            "difficult": difficult,
            "components":components,
            "set": set, "complete": 0}
        return
    
    tasks[name] = {
        "deadline": deadline,
        "note": note,
        "difficult": difficult,
        "set": set, "complete": 0}
    return

def bubble_sort(list):
    for iter in range(len(list)):
        for index in range(iter):
            current = list[index]
            next = list[index + 1]
            if current > next:
                list[index], list[index + 1] = next, current
    return list
