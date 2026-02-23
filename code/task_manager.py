import json
import datetime


def get_json(file):
    """Возвращает словарь

    :param file: путь к файлу(можно не указывать формат файла, потому что функция только для json)
    """
    file = "jsons/"+file
    file = file + ".json" if not file.endswith(".json") else file
    with open(file, "r", encoding="UTF-8") as file_in:
        result = json.load(file_in)
    return result

def upd_json(file, content:dict):
    """Записывает данные content в file(json)

    :param file: путь до файла(можно не указывать формат файла, потому что функция только для json)
    :param content: запысываемый словарь"""
    file = "jsons/"+file
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

    easy = 30 # 30 минут
    midl = 60 # час
    hard = 240 # 4 часа
    diff = difficult
    if not diff:
        if estime <= easy: 
            diff = "easy"
        elif estime <= midl:
            diff = "midl"
        elif estime <= hard:
            diff = "hard"
        elif estime > hard:
            diff = "complex"
    if diff == "complex":
        if not components:
            components = {}
            print(f"У комплексной задачи должны быть подзадачи")
            sub_tasking()
    
    if main and components:
        return {"difficult":diff, "deadline":deadline, "estime":estime, "note":note, "components":components, "set":set, "complete":0.0}
    elif main:
        return {"difficult":diff, "deadline":deadline, "estime":estime, "note":note, "set":set, "complete":0.0}
    else:
        return {"difficult":diff, "estime":estime, "note":note, "complete":0.0}

def task_filter(arg:str="complete", rule="<", filtermark=1,  prim_dict:dict=get_json("tasks")):
    """
    Возврачает список ключей, подходящих по условию
    
    :param arg: Параметр задачи
    :type arg: str
    :param rule: Логических знак > < ==
    :type rule: str
    :param filtermark: Значение для сравнения
    :param prim_dict: Словарь задач
    :type prim_dict: dict
    """
    if rule not in ["<", ">", "==", "!=", ">=", "<="]:
        return
    list = []
    checked = []
    
    for key in prim_dict:
        if not(arg == "components"):
            list.append({key:prim_dict[key][arg]})
        else:
            if "components" in prim_dict[key]:
                list.append({key:len(prim_dict[key][arg].keys())})

    if arg == "difficult":
        difficults = ["easy", "midl", "hard", "complex"]
        limit = -1
        for i, elem in enumerate(difficults):
            if elem == filtermark:
                limit = i
                break
        if not (limit < 0):
            if rule == "<":
                difficults = difficults[0:limit]
            elif rule == ">":
                difficults = difficults[limit+1::]
            else: #rule == "=="
                difficults = difficults[limit] 
    elif arg == "deadline":
        filtermark = str(datetime.date.today()).split("-") if not filtermark else filtermark.split(".") #today if not filtermark
        filtermark = [int(dd) for dd in filtermark[::-1]]

    for dict in list:
        correct = False
        for key in dict:
            val = str(dict[key])
            if arg in ["estime", "components"]:
                correct = True if eval(f"{val} {rule} {str(filtermark)}") else False

            elif arg == "difficult":
                if dict[key] in difficults:
                    correct = True
                    
            elif arg == "complete":
                """
                <1 не выполненные
                >0 начатые
                ==0 не начатые
                ==1 выполненные
                >0.33 Выполненные больше чем на 0.33
                <0.66 Выполненные меньше чем на 0.66
                ==0.5 Выполненные строго на половину
                """
                ex = f"{float(val)} {rule} {float(filtermark)}"
                expression = eval(ex) if not (float(val) == 1.0 and rule == ">") else False
                correct = True if expression else False

            elif arg == "deadline":
                """
                < Просроченные
                == Четкое совпадение
                >= Не просроченные
                """
                value = [int(num) for num in val.split(".")[::-1]] #Что сравнивается
                date = filtermark[::-1] #С чем сравнивается
                rating = [0, 0, 0]
                for i in range(3):
                    rating[i] = value[i] - date[i]
                date_check = False
                if eval(f"{rating[0]} {rule} 0"):
                    date_check = True
                elif eval(f"{rating[0]} {rule[0]}= 0") and eval(f"{rating[1]} {rule} 0"):
                    date_check = True
                elif eval(f"{rating[0]} {rule[0]}= 0") and eval(f"{rating[1]} {rule[0]}= 0") and eval(f"{rating[2]} {rule} 0"):
                    date_check = True    
                correct = date_check
                
                        
        if correct:
            checked.append({key:val})
    result = [0]*len(checked)
    for index, dict in enumerate(checked):
        for key in dict:
            result[index] = key      
    return result

def bubble_sort(list):
    """Возвращает список, отсортированый методом пузырька"""
    for iter in range(len(list)):
        for index in range(iter):
            current = list[index]
            next = list[index + 1]
            if current > next:
                list[index], list[index + 1] = next, current
    return list
