"""Повестка дня
Удалить повторы \n 
Придумать реализацию сроков"""


nav_panel = """[1] - Новая задача
[2] - Ближайшие задачи
[3] - Все задачи"""


def task_manager(n):
    """Принимает на вход число"""
    file = open("tasks.txt", "+a", encoding="UTF-8")

    if n == 1: #Добавляет задачу в файл tasks.txt
        tasks = file.read()
        while (text := input()) != "":
            tasks += "\n" + text
        file.write(tasks)        
    elif n == 2:
        pass
    elif n == 3: # Выводит в консоль список всех задач
        file.seek(0)
        print(file.read())
    
    file.close()


print(nav_panel)
while (cur_action := int(input("Ввод: "))) > 0:
    task_manager(cur_action)

