from sqlite_db import SQLiteDB
from json_loader import JSONLoader
from base_model import Param

def main():
    db = SQLiteDB("my_data.db")
    data = JSONLoader.load_from_file("storage/data.json", Param)
    db.insert_many(data)

if __name__ == "__main__":
    main()
