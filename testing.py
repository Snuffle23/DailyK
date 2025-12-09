for i in range(3):
    
    file = open("tasks.txt", "+a",encoding="UTF-8")
    file.seek(0)
    tasks = file.read()
    print(tasks)

    n = int(input())
    
    if n == 1: #Добавляет задачу в файл tasks.txt
        tasks += "\n" + input()
        file.write(tasks)        
    elif n == 2:
        pass
    elif n == 3: # Выводит в консоль список всех задач
        print(tasks)
    
    file.close()