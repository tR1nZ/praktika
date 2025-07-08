from sqlite_storage import SqliteStorage

def main():
    db = SqliteStorage("my_data.db")
    db.import_from_json("storage/data.json", "storage/storbe.json")

if __name__ == "__main__":
    main()
