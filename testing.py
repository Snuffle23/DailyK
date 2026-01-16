import json, datetime
from task_manager import *
def dtools(choise:int=1):
    """
    Docstring для etool
    
    :param choise: Выбор номера 
    :type choise: int
    :param tasks: Доп параметры для функций
    """
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

    if choise == 1:
        show_tasks()
    elif choise == 2:
        add_task()

def initialization():
    pass

def task_filter(arg:str="complete", rule="==", filtermark=False,  prim_dict:dict=get_json("tasks")):
    """
    Возврачает список ключей
    
    :param arg: Описание
    :type arg: str
    :param rule: Описание
    :type rule: str
    :param filtermark: Описание
    :param prim_dict: Описание
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
                if rating[0] < 0:
                    date_check = True
                elif rating[0] <= 0 and rating[1] < 0:
                    date_check = True
                elif rating[0] <= 0 and rating[1] <= 0 and rating[2] < 0:
                    date_check = True

                if rule == "==":
                    for i in rating:
                        date_check = True if i == 0 else False
                elif rule == ">=":
                    date_check = True if date_check == False else False
                correct = date_check
                        
        if correct:
            checked.append({key:val})
    result = [0]*len(checked)
    for index, dict in enumerate(checked):
        for key in dict:
            result[index] = key      
    return result

for i in range(1):
    print(task_filter(input("Аргумент: "), input("Правило: "), input("Маркер: ")))
