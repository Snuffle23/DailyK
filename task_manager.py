import json
import datetime


def get_json(file):
    """Возвращает словарь

    :param file: путь к файлу(можно не указывать формат файла, потому что функция только для json)
    """
    file = file + ".json" if not file.endswith(".json") else file
    with open(file, "r", encoding="UTF-8") as file_in:
        result = json.load(file_in)
    return result

def upd_json(file, content:dict):
    """Записывает данные content в file(json)

    :param file: путь до файла(можно не указывать формат файла, потому что функция только для json)
    :param content: запысываемый словарь"""

    file = file + ".json" if not file.endswith(".json") else file
    with open(file, 'w', encoding="UTF-8") as file_out:
        json.dump(content, file_out, ensure_ascii=False, indent=4)

def name_normalize(name:str="", dict={}):
        """Возвращает нормализированную строку (без пробелов в начале и в конце), добавляет _num, чтобы получить строку, подходящую как ключ для словаря dict"""
        
        while name.endswith(" "):#срез строки без последнего символа, пока кончается на пробел
            name = name[0:-1]
        while name.startswith(" "):#срез строки без первого символа, пока начинается на пробел
            name = name[1::]

        while name in dict.keys():
            elems = name.split("_")
            digit_end = f"_{int(elems[-1]) + 1}" if (elems[-1].isdigit()) else "_1"
            name = ("_".join(elems[:-1:] if len(elems) > 1 else elems) )+ digit_end
        return name


def tasking(estime:int=1, deadline:str=False, note:str=False, difficult:str=False, components = False, main:bool=True):
    """Возвращает словарь с данными задачи

    :param estime: Описывает время в минутах, требующееся для выполнения задачи. 
    Из него расчитывается сложность задачи.
    :param deadline: Крайний срок задачи. Не может быть прошедшей датой.
    :param note: Описание задачи (необязательное)
    :param difficult: Задаёт сложность задачи. Используется в тех случаях, когда тип задачи не соответсвует расчетному времени.
    :param components: Словарь подзадач, будет использован при создании сложной задачи.
    :param main: Определяет структуру заполнения выходного словаря. True для основных задач False для подзадач.
    """

    def sub_tasking():
        while (sub_name:= input(f"Имя позадачи {len(components.keys()) + 1}: ")) != "":
            while (sub_estime:=input("Расчетное время: ")) != "":
                if sub_estime.isdigit():
                    if int(sub_estime) > hard:
                        print("Время выходит за диапозон. Укажите меньше 120 минут")
                    else:
                        break
                else:
                    print("Введите число")
            sub_note = input("Описание: ")
            components[name_normalize(sub_name, components)] = tasking(int(sub_estime), note=sub_note, main=False)
        if len(components.keys()) < 1:
            sub_tasking()

    set = (datetime.date.today()).strftime("%d.%m.20%y")
    components = {} if not components else components

    easy = 30 # 30 минут
    midl = 60 # час
    hard = 240 # 4 часа
    if estime <= easy: 
        diff = "easy"
    elif estime <= midl:
        diff = "midl"
    elif estime <= hard:
        diff = "hard"
    elif estime > hard or difficult == "complex":
        diff = "complex"
        print(f"У комплексной задачи должны быть подзадачи")
        sub_tasking()
    
    if main and components:
        return {"difficult":diff, "deadline":deadline, "estime":estime, "note":note, "components":components, "set":set, "progress":0.0, "complete":0}
    elif main:
        return {"difficult":diff, "deadline":deadline, "estime":estime, "note":note, "set":set, "complete":0}
    else:
        return {"difficult":diff, "estime":estime, "note":note, "complete":0}

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


def bubble_sort(list):
    """Возвращает список, отсортированый методом пузырька"""
    for iter in range(len(list)):
        for index in range(iter):
            current = list[index]
            next = list[index + 1]
            if current > next:
                list[index], list[index + 1] = next, current
    return list
