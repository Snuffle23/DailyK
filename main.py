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

def tasking(year=None,month=None, day=None, content:dict=None):
    if year is None: year=today()[0]
    else: year = str(year)
    if month is None: month=today()[1]
    else: month = str(month)
    if day is None: day=today()[2]
    else: day = str(day)
    if content is not None:
        content["set"] = today()
        content["deadline"] = (year,month,day)
        content["complete"] = 0
        if _calen.attach(year,month,day, _tasks.new(content=content), 0):
            print("- New task created. -\n")
        else:
            print("A DateErrore has occerred! The task wasn't created. ")
    else:
        print("Content atr should not be empty!")


def remove_task():
    #year=None,month=None, day=None, content=None
    #if year is None: year=today()[0]
    #if month is None: month=today()[1]
    #if day is None: day=today()[2]
    pass
    

class DayEntry:
    groups = ["tasks"]
    def __init__(self):
        print(f"---celendar initiated:'{datetime.now()}'---")
        self.cal = get_json("jsons/calendar.json")
        self.date_init()
 
    def date_init(self, year=None, month=None, day=None):
        if year is None: year=today()[0]
        else: year = str(year)
        if month is None: month=today()[1]
        else: month = str(month)
        if day is not None:day = str(day)

        dictionary = self.cal
        rule = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

        if year not in dictionary.keys():
            dictionary[year] = {}
            print(f"Creating year section - '{year}'" + ":{}...")

        if month not in dictionary[year].keys():
            if int(month) < 13:
                dictionary[year][month] = {}
                print(f"Creating month section - '{year}.{month}'" + ":{}...")
            else:
                print("The month must be greater than 13")
                return False
        if day is not None:
            if day not in list(dictionary[year][month].keys()):
                if int(day) < max(calendar.monthcalendar(int(year),int(month))[-1]):
                    dictionary[year][month][day] = (rule[calendar.weekday(int(year), int(month), int(day))], {})
                    print(f"Creating day section - '{year}.{month}.{day}'" + ":{}...")
                else:
                    print("Day must be exist!")
                    return False
            else:
                print("Day already was created.")
                return None

        if day is None:
            if len(list(dictionary[year][month].keys())) < max(calendar.monthcalendar(int(year),int(month))[-1]):
                weeks = calendar.monthcalendar(int(year),int(month))
                for week in weeks:
                    for indx, day_of_week in enumerate(week):
                        if day_of_week != 0:
                            if str(day_of_week) not in dictionary[year][month].keys():
                                dictionary[year][month][str(day_of_week)] = [rule[indx], {}]
                print(f"Creating days 1 - {max(weeks[-1])} in {year}.{month}...")
            else:
                print("All available days already was created.\n")
                return False
        print("- successful initialization -\n")
        load_json("jsons/calendar.json", dictionary)
        self.cal = get_json("jsons/calendar.json")


    def get():
        pass


    def attach(self,year, month, day, task_id:str, group_number:int):
        year, month, day = map(str, [year,month, day])
        if self.date_init(year, month, day) is not None:
            _tasks.remove(task_id)
            return
        date = self.cal[year][month][day][1]
        group = self.groups[group_number]

        if group not in date.keys():
            date[group] = []
            print("group created")

        if task_id not in date[group]:
            date[group].append(task_id)
            print("the task_id was added to date")
        else:
            print("the task_id is already attached")

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

    def get_by_attr(self, attr):
        pass

    def new(self,content):
        id = 1
        while str(id) in self.ids: id+=1
        self.all[id] = content
        

        load_json("jsons/tasks.json", self.all)
        self.self_upd()
        return id
    
    def remove(self,id):
        print(f"{self.all.pop(str(id),'Task don\'t was')} deleted")
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
    

_calen = DayEntry()
_tasks = Tasks()