class Statements:

    @staticmethod
    def create_table():
        return ('''CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY,
                name TEXT,
                city TEXT,
                salary_bottom TEXT,
                salary_top TEXT,
                published_at TEXT,
                employer_name TEXT,
                key_skills TEXT,
                schedule TEXT,
                professional_role TEXT,
                experience TEXT)''')

    @staticmethod
    def insert_vacancy():
        return (f'''INSERT INTO vacancies
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        ''')

    @staticmethod
    def check_table():
        return """SELECT id FROM vacancies LIMIT 1"""
