import sqlite3
import json


class SqliteStorage:
    def __init__(self, db_path: str = "data.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS param (
                nl INTEGER,
                n1grs INTEGER,
                distr TEXT,
                is_am INTEGER,
                kgd INTEGER,
                kgrs INTEGER,
                ndec INTEGER,
                nfgd_fu INTEGER,
                samples_num INTEGER,
                shgd INTEGER,
                true_nins INTEGER
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS time (
                cpu_test REAL,
                fft REAL,
                read_data REAL,
                sine REAL,
                write REAL,
                total REAL,
                date TEXT,
                time TEXT
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS verif (
                valid INTEGER,
                verif_data TEXT
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS strobe (
                array TEXT
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS output (
                out_arr TEXT,
                out_verif TEXT
            )
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS data (
                polar INTEGER,
                path TEXT,
                param_id INTEGER,
                time_id INTEGER,
                verif_id INTEGER,
                strobe_id INTEGER,
                output_id INTEGER,
                json_raw TEXT,
                FOREIGN KEY (param_id) REFERENCES param(id),
                FOREIGN KEY (time_id) REFERENCES time(id),
                FOREIGN KEY (verif_id) REFERENCES verif(id),
                FOREIGN KEY (strobe_id) REFERENCES strobe(id),
                FOREIGN KEY (output_id) REFERENCES output(id)
            )
        ''')

        self.conn.commit()

    def import_from_json(self, data_path: str, strobe_path: str):
        with open(data_path) as f:
            data_json = json.load(f)

        with open(strobe_path) as f:
            strobe_json = json.load(f)

        cur = self.conn.cursor()

        # PARAM
        params = data_json["params"]
        param_values = (
            params.get("distr"),
            params.get("is_am"), params.get("kgd"), params.get("kgrs"),
            params.get("n1grs"),
            params.get("ndec"), params.get("nfgd_fu"),
            params.get("nl"),
            params.get("samples_num"), params.get("shgd"),
            params.get("true_nihs")
        )
        cur.execute('''
            INSERT INTO param (nl, n1grs, distr, is_am, kgd, kgrs, ndec, nfgd_fu,
                               samples_num, shgd, true_nins)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', param_values)
        param_id = cur.lastrowid

        # TIME
        time = data_json["time"]
        time_values = (
            time["cpu_testing_time"]["duration"],
            time["fft"]["duration"],
            time["read_data"]["duration"],
            time["sine"]["duration"],
            time["write_data"]["duration"],
            time["total"]["duration"],
            time["date"],
            time["time"]
        )
        cur.execute('''
            INSERT INTO time (cpu_test, fft, read_data, sine, write, total, date, time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', time_values)
        time_id = cur.lastrowid

        # VERIFICATION
        verif = data_json["verification"]
        is_valid = verif.get("is_data_valid", 0)
        verif_data_json = json.dumps(verif.get("out_verif", []))
        cur.execute('''
            INSERT INTO verif (valid, verif_data)
            VALUES (?, ?)
        ''', (is_valid, verif_data_json))
        verif_id = cur.lastrowid

        # STROBE
        strobe_array = list(strobe_json.values())[0]  # use first (and only) array
        strobe_str = json.dumps(strobe_array)
        cur.execute('''
            INSERT INTO strobe (array)
            VALUES (?)
        ''', (strobe_str,))
        strobe_id = cur.lastrowid

        # OUTPUT
        cur.execute('''
            INSERT INTO output (out_arr, out_verif)
            VALUES (?, ?)
        ''', (strobe_str, verif_data_json))
        output_id = cur.lastrowid

        # DATA
        cur.execute('''
            INSERT INTO data (polar, path, param_id, time_id, verif_id, strobe_id, output_id, json_raw)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data_json["polar"], data_json["report_path"],
            param_id, time_id, verif_id, strobe_id, output_id,
            json.dumps(data_json)
        ))

        self.conn.commit()
        print("данные успешно импортированы в базу данных")

