class CollectorStatements:

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
        return """SELECT id FROM vacancies ORDER BY id ASC LIMIT 1"""


class AnalyticStatements:
    @classmethod
    def choose_statement(cls, statement):
        statements = {
            'get_salary_by_role': cls.get_salary_by_role(),
            'get_salary_by_city': cls.get_salary_by_city(),
        }
        method = statements.get(statement)
        return method()
    @staticmethod
    def get_salary_by_role():
        return ("""
        SELECT
            professional_role,
            salary_bottom,
            salary_top
        FROM vacancies
        """)

    @staticmethod
    def get_salary_by_city():
        return ("""
        SELECT
            city,
            salary_bottom,
            salary_top
        FROM vacancies
        """)