import json, datetime
from task_manager import *



def sort_task(tasks, arg):
    """Возвращает список ключей указанного словоря в осортированном порядке"""
    dict = {}
    result = []
    res = {}
    for task in tasks:#словарь имя:дата потом сопоставить значения
        date = tasks[task][arg].split(".")
        res[task] = tasks[task][arg]
        if date[2] not in dict:# добавляем год
            dict[date[2]] = {}
        if date[1] not in dict[date[2]]:# добавляем месяц
            dict[date[2]][date[1]] = []
        dict[date[2]][date[1]].append(date[0])# Добавляем дни

    for year in dict:# Отсортированные месяца сопоставить с ключами и не потерять значения
        months = {}
        sorted_months = []
        for month in dict[year]:
            sorted_months.append(month)
            dict[year][month] = bubble_sort(dict[year][month])
        for m in bubble_sort(sorted_months):
            months[m] = dict[year][m]
        dict[year] = months

    for year in dict:
        for month in dict[year]:
            for day in dict[year][month]:
                result.append(f"{day}.{month}.{year}")
    sorted = False

    answ = []
    while not sorted:
        for date in result:
            for r in res:
                for i in range(len(result)):
                    if res[r] == date:
                        answ.append(f"{r}:{result.pop(i)}")
                        break
        if len(res.keys()) == len(answ):
            sorted = True
    return answ


arg = "deadline"
tasks = get_json("tasks.json")
for task in tasks:
    print(f"{task}:{tasks[task][arg]}")
print("---"*20)
for i in sort_task(tasks, arg):
    print(i)

        
