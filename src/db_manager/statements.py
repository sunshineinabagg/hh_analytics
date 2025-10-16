class CollectorStatements:

    @staticmethod
    def create_table():
        return ('''CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY,
                name TEXT,
                city TEXT,
                salary_bottom TEXT,
                salary_top TEXT,
                currency TEXT,
                published_at TEXT,
                employer_name TEXT,
                key_skills TEXT,
                schedule TEXT,
                professional_role TEXT,
                experience TEXT)''')

    @staticmethod
    def insert_vacancy():
        return (f'''INSERT INTO vacancies
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
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
            'get_roles_count': cls.get_roles_count(),
            'get_salary_by_experience': cls.get_salary_by_experience(),
            'get_key_skills': cls.get_key_skills(),
            'get_schedule_analysis': cls.get_schedule_analysis(),
            'get_vacancy_dynamics': cls.get_vacancy_dynamics(),
            'get_employer_analysis': cls.get_employer_analysis()
        }
        method = statements.get(statement)
        return method

    @staticmethod
    def get_salary_by_role():
        return ("""
        SELECT
            vacancies.professional_role,
            salary_bottom,
        salary_top,
        currency,
        vac_count.count
        FROM vacancies
        JOIN (
            SELECT professional_role, COUNT(id) as count
            FROM vacancies
            GROUP BY professional_role
        ) as vac_count
        ON
            vacancies.professional_role = vac_count.professional_role
        WHERE
            currency = '"RUR"'
            AND salary_bottom != '"None"'
            AND salary_top != '"None"'
        """)

    @staticmethod
    def get_salary_by_city():
        return ("""
        SELECT
            v.city,
            v.salary_bottom,
            v.salary_top,
            v.currency,
            c.total_vacancies
        FROM vacancies AS v
        JOIN (
            SELECT city, COUNT(id) as total_vacancies
            FROM vacancies
            WHERE city != '"None"'
            GROUP BY city
        ) as c
        ON v.city = c.city
        WHERE
            v.currency = '"RUR"'
            AND v.salary_bottom != '"None"'
            AND v.salary_top != '"None"'
            AND v.city != '"None"'
        """)

    @staticmethod
    def get_roles_count():
        return ("""
        SELECT
            professional_role,
            COUNT(id) AS count_vacancies
        FROM vacancies
        GROUP BY professional_role
        """)

    @staticmethod
    def get_salary_by_experience():
        return ("""
        SELECT
            v.experience,
            v.professional_role,
            v.salary_bottom,
            v.salary_top,
            v.currency,
            total.total_vacancies
        FROM vacancies AS v
        JOIN (
            SELECT experience, professional_role, COUNT(*) AS total_vacancies
            FROM vacancies
            GROUP BY experience, professional_role
        ) AS total
        ON v.experience = total.experience AND v.professional_role = total.professional_role
        WHERE
            v.currency = '"RUR"'
            AND v.salary_bottom != '"None"'
            AND v.salary_top != '"None"'

        """)

    @staticmethod
    def get_key_skills():
        return ("""
        SELECT
            professional_role,
            key_skills
        FROM vacancies
        WHERE
            key_skills != '"None"'
        """)

    @staticmethod
    def get_schedule_analysis():
        return ("""
        SELECT
            v.schedule,
            v.salary_bottom,
            v.salary_top,
            v.currency,
            v.published_at,
            total.total_vacancies
        FROM vacancies AS v
        JOIN (
            SELECT schedule, COUNT(*) AS total_vacancies
            FROM vacancies
            GROUP BY schedule
        ) AS total
        ON v.schedule = total.schedule
        """)

    @staticmethod
    def get_vacancy_dynamics():
        return ("""
        SELECT
            published_at,
            salary_bottom,
            salary_top,
            currency,
            professional_role
        FROM vacancies
        """)

    @staticmethod
    def get_employer_analysis():
        return ("""
        SELECT
            employer_name,
            professional_role,
            key_skills,
            salary_bottom,
            salary_top,
            currency
        FROM vacancies
        """)
