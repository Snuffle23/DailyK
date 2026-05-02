import json
import calendar
from datetime import datetime
#pyside6-designer for UI on future


def get_json(path):
    """Возвращает словарь

    :param path: путь к файлу
    """
    with open(path, "r+", encoding="UTF-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            file.seek(0)
            json.dump({}, file, ensure_ascii=False, indent=4)
            return {}

def load_json(path, data:dict):
    """Записывает данные в file.json

    :param file: путь до файла
    :param data: запысываемый словарь"""
    with open(path, "w", encoding="UTF-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def today():
    now = datetime.now()
    return str(now.year), str(now.month), str(now.day)

def tasking(year=None,month=None, day=None, content=None):
    if year is None: year=today()[0]
    if month is None: month=today()[1]
    if day is None: day=today()[2]
    if not(content is None):
        date.attach(2026, 5, 2, tasks.new(content), 0)

class DayEntry:
    created_at = datetime.now()
    groups = ["tasks"]
    def __init__(self):
        print(f"---celendar initiated:'{self.created_at}'---\n")
        self.cal = get_json("jsons/calendar.json")
        self.date_init()
 
    def date_init(self, year=created_at.year, month=created_at.month, day=""):
        year, month, day = map(str, [year,month, day])
        dictionary = self.cal
        rule = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

        if year not in dictionary.keys():
            dictionary[year] = {}
            print(f"Created new section - '{year}'" + ":{}")

        if month not in dictionary[year].keys():
            dictionary[year][month] = {}
            print(f"Created new section - '{year}.{month}'" + ":{}")

        if day and (day not in dictionary[year][month].keys()):
            dictionary[year][month][day] = (rule[calendar.weekday(int(year), int(month), int(day))], {})
            print(f"Created new section - '{year}.{month}.{day}'" + ":{}")
        
        if not day:
            
            weeks = calendar.monthcalendar(int(year),int(month))
            for week in weeks:
                for i, day in enumerate(week):
                    if day != 0:
                        if str(day) not in dictionary[year][month].keys():
                            dictionary[year][month][str(day)] = [rule[i], {}]
        
        load_json("jsons/calendar.json", dictionary)
        self.cal = get_json("jsons/calendar.json")


    def get(self, year=created_at.year, month=created_at.month, day=created_at.day):
        year, month, day = map(str, [year, month, day])
        try:
            return self.cal[year][month][day]
        except KeyError:
            print("Date not found for giving")


    def attach(self,year, month, day, content:str, group_number:int):
        year, month, day = map(str, [year,month, day])
        self.date_init(year, month, day)
        date = self.cal[year][month][day][1]
        group = self.groups[group_number]

        if group not in date.keys():
            date[group] = []
            print("group created")

        if content not in date[group]:
            date[group].append(content)
            print("the content was added to date")
        else:
            print("the content is already attached")

        self.cal[year][month][day][1] = date
        load_json("jsons/calendar.json", self.cal)

    def remove(self,year, month, day, content:str, group_number:int):
        year, month, day = map(str, [year,month, day])
        group = self.groups[group_number]
        attached = self.cal[year][month][day][1][group] #{'tasks': ['3']}
        try:
            attached.remove(content)
            print("the content was deleted")
        except:
            print("content not exist for this date")

        self.cal[year][month][day][1][group] = attached
        load_json("jsons/calendar.json", self.cal)


class Tasks:
    def __init__(self):
        self.self_upd()#Подгрузка
        self.sort_file()#Сортировка
        self.self_upd()#Обновление

    def self_upd(self):
        """Обновляет полный список задач и id"""
        self.all = get_json("jsons/tasks.json")
        self.ids = list(self.all.keys())

    def sort_file(self):
        """Располагает задачи в порядке возрастания id. Меняет исходный файл."""
        new_file = {}
        ids = sorted(self.ids)
        for id in ids: new_file[id] = self.all[id]
        load_json("jsons/tasks.json",new_file)

    def get(self,id):
        if str(id) in self.ids:
            print("got")
            print(self.all[str(id)])
        else:
            print(f"Task with ID:'{id}' not exist")

    def get_by_attr(self, attr, val):
        pass

    def new(self,content):
        id = 1
        while str(id) in self.ids: id+=1
        self.all[id] = content
        

        load_json("jsons/tasks.json", self.all)
        self.self_upd()
        return id
    
    def remove(self,id):
        print(f"{self.all.pop(str(id),"Task don't was")} deleted")
        load_json("jsons/tasks.json", self.all)
        self.self_upd()


    def name_normalize(self, name="Some task"):
        """Возвращает нормализированную строку (без пробелов в начале и в конце)"""
        name = str(name)
        while name.endswith(" "):#срез строки без последнего символа, пока кончается на пробел
            name = name[0:-1]
        while name.startswith(" "):#срез строки без первого символа, пока начинается на пробел
            name = name[1::]
        return name

tasks = Tasks()
date = DayEntry()
content = {
        "name":"XXX",
        "difficult":"",
        "deadline":"",
        "note":"",
        "set":"",
        "complete":""
        }

tasking(content=content)


