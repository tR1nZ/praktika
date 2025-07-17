from storage.sqlite_db import SQLiteDB
from storage.json_loader import JSONLoader
from storage.base_model import Param

def main():
    db = SQLiteDB("my_data.db")
    data = JSONLoader.load_from_file("examples/data.json", Param)
    db.insert_many(data)

if __name__ == "__main__":
    main()
