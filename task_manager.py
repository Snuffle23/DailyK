import json
import datetime


def get_json(file):
    """Возвращает словарь

    :param file: путь к файлу
    """

    with open(file, "r", encoding="UTF-8") as file_in:
        result = json.load(file_in)
    return result

def upd_json(file, content:dict):
    """Записывает данные content в file(json)

    :param file: путь до файла
    :param content: запысываемый словарь"""
    with open(file, 'w', encoding="UTF-8") as file_out:
        json.dump(content, file_out, ensure_ascii=False, indent=4)


def name_normalize(name:str=""):
    """Возвращает нормализированную строку (без пробелов в начале и в конце)
    
    :param name: Строка 
    """
    while name != "":#Генерация и проверка имени
        if name.startswith(" ") or name.endswith(" "):
            while name.endswith(" "):
                name = name[0:-2]
            while name.startswith(" "):
                name = name[1::]
        break
    return name

def overdue_checkup(tasks:dict, overdue=False, arg="deadline"):
    """
    Возвращает словарь {task:date}

    :param tasks: Список проверяемых задач
    :param overdue: срок годности. True - просроченные, False - непросроченные
    """
    today = datetime.date.today().strftime(f"%d.%m.20%y").split(".")[::-1]
    checked = {}
    for task in tasks:
        if arg:
            date = tasks[task][arg]
        else:
            date = tasks[task]
        overdue_mark = False
        for i, d in enumerate(date.split(".")[::-1]):#индекс и элемент даты
            if int(d) < int(today[i]) and int(date.split(".")[1]) <= int(today[1]):
                overdue_mark = True
        if overdue_mark == overdue:
            checked[task] = date
    return checked

def arg_checkup(tasks:dict, arg:str, value=""):
    """
    Возвращает список имен, содержащих значение агрумента
    
    :param tasks: Итерируемый словарь
    :param arg: Ключ, по которому проверяется значение в итерируемом словаре
    :param value: проверяемое значение
    """
    
    final_list = []
    for task_name in tasks:
        task_dict = tasks[task_name]
        if task_dict.get(arg, "Not found") != "Not found":
            if value and str(task_dict[arg]) == value:
                final_list.append(task_name)
    return final_list

def create_task(tasks:dict={}): #реализовать множественное создание задач
    """Добавляет задачу в указанный словарь""" 
    name = name_normalize(input("Название: "))
    while not (name not in tasks.keys()) and (name != ""):
        name = name_normalize(input("Попробуйте другое: "))
    if not name:
        return
    #Генерация контента
    set = (datetime.date.today()).strftime("%d.%m.%y")
    deadline = input("Дедлайн: ")
    note = input("Описание: ")
    difficult = {1:"easy", 2:"midl", 3:"hard", 4:"comp"}[int(num)] if ((num:=input("Сложность 1-4: ")) < "5") and num.isdigit() else 1
    if difficult == "comp":
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
    """Возвращает список, отсортированый методом пузырька"""
    for iter in range(len(list)):
        for index in range(iter):
            current = list[index]
            next = list[index + 1]
            if current > next:
                list[index], list[index + 1] = next, current
    return list
