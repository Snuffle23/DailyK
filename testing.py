import json, datetime

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
        json.dump(content, file_out, ensure_ascii=False, indent=2)
