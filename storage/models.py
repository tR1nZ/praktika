import json

class Param:
    def __init__(self, distr, is_am, kgd, kgrs, n1grs, ndec, nfgd_fu, nl, samples_num, shgd, true_nins):
        self.distr = distr
        self.is_am = is_am
        self.kgd = kgd
        self.kgrs = kgrs
        self.n1grs = n1grs
        self.ndec = ndec
        self.nfgd_fu = nfgd_fu
        self.nl = nl
        self.samples_num = samples_num
        self.shgd = shgd
        self.true_nins = true_nins

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS param (
                distr TEXT,
                is_am BOOLEAN,
                kgd INTEGER,
                kgrs INTEGER,
                n1grs INTEGER,
                ndec INTEGER,
                nfgd_fu INTEGER,
                nl INTEGER,
                samples_num INTEGER,
                shgd INTEGER,
                true_nins INTEGER
            )
        """)

    @staticmethod
    def from_dict(d):
        return Param(**d)

    def to_tuple(self):
        return (self.distr, self.is_am, self.kgd, self.kgrs, self.n1grs, self.ndec,
                self.nfgd_fu, self.nl, self.samples_num, self.shgd, self.true_nins)


class Time:
    def __init__(self, cpu_test, date, fft, read_data, sine, time, total, write):
        self.cpu_test = cpu_test
        self.date = date
        self.fft = fft
        self.read_data = read_data
        self.sine = sine
        self.time = time
        self.total = total
        self.write = write

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS time (
                cpu_test REAL,
                date TEXT,
                fft REAL,
                read_data REAL,
                sine REAL,
                time REAL,
                total REAL,
                write REAL
            )
        """)

    @staticmethod
    def from_dict(d):
        return Time(**d)

    def to_tuple(self):
        return (self.cpu_test, self.date, self.fft, self.read_data, self.sine, self.time, self.total, self.write)


class Verif:
    def __init__(self, valid, out_verif, src, verif_data):
        self.valid = valid
        self.out_verif = out_verif
        self.src = src
        self.verif_data = verif_data

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verif (
                valid BOOLEAN,
                out_verif TEXT,
                src TEXT,
                verif_data TEXT
            )
        """)

    @staticmethod
    def from_dict(d):
        return Verif(**d)

    def to_tuple(self):
        return (self.valid, self.out_verif, self.src, self.verif_data)


class Strobe:
    def __init__(self, values):
        self.values = values  # список

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS strobe (
                values TEXT
            )
        """)

    @staticmethod
    def from_dict(arr):
        return Strobe(arr)

    def to_tuple(self):
        return (json.dumps(self.values),)


class Output:
    def __init__(self, out_arr, out_verif):
        self.out_arr = out_arr
        self.out_verif = out_verif

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS output (
                out_arr TEXT,
                out_verif TEXT
            )
        """)

    @staticmethod
    def from_dict(d):
        return Output(d.get("out_arr"), d.get("out_verif"))

    def to_tuple(self):
        return (json.dumps(self.out_arr), self.out_verif)


class Data:
    def __init__(self, param_id, time_id, verif_id, strobe_id, output_id, polar, path):
        self.param_id = param_id
        self.time_id = time_id
        self.verif_id = verif_id
        self.strobe_id = strobe_id
        self.output_id = output_id
        self.polar = polar
        self.path = path

    @staticmethod
    def create_table(cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data (
                param_id INTEGER,
                time_id INTEGER,
                verif_id INTEGER,
                strobe_id INTEGER,
                output_id INTEGER,
                polar TEXT,
                path TEXT,
                FOREIGN KEY(param_id) REFERENCES param(id),
                FOREIGN KEY(time_id) REFERENCES time(id),
                FOREIGN KEY(verif_id) REFERENCES verif(id),
                FOREIGN KEY(strobe_id) REFERENCES strobe(id),
                FOREIGN KEY(output_id) REFERENCES output(id)
            )
        """)

    def to_tuple(self):
        return (self.param_id, self.time_id, self.verif_id, self.strobe_id, self.output_id, self.polar, self.path)
