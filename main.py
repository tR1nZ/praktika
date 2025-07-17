from storage.sqlite_db import SQLiteDB
from storage.json_loader import JSONLoader
from storage.models import Param

def main():
    db = SQLiteDB("my_data.db")
    params = JSONLoader.load_from_file("examples/data.json", Param)
    db.insert_many([params]) # принимает List -> оборачиваем в скобки


if __name__ == "__main__":
    main()
