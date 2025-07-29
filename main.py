from storage.sqlite_db import SQLiteDB
from storage.json_loader import JSONLoader
from storage.models import Param, Time

def main():
    db = SQLiteDB("my_data.db")
    params = JSONLoader.load_from_file("examples/in_args.json", Param)
    db.create([params])
    db.insert_many([params]) # принимает List -> оборачиваем в скобки
    #Times = Time(0,0,0,0,0,0,0,0)
    #print(Times.__dict__.items())


if __name__ == "__main__":
    main()
