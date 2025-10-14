import pandas as pd

from src.db_manager.db import Database

class Analyzator:
    def __init__(self, db: Database):
        self._db = db

    def analyze_salaries_by_role(self):
        raw_data = self._db.select_for_analytics('get_salary_by_role')

        df = pd.DataFrame(raw_data, columns=['professional_role', 'salary_bottom', 'salary_top'])
        df['salary_bottom'] = pd.to_numeric(df['salary_bottom'], errors='coerce')
        df['salary_top'] = pd.to_numeric(df['salary_top'], errors='coerce')
        df = df.dropna(subset=['salary_bottom', 'salary_top'])

        summary = df.groupby('professional_role').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            median_salary_bottom=('salary_bottom', 'median'),
            median_salary_top=('salary_top', 'median'),
            min_salary=('salary_bottom', 'min'),
            max_salary=('salary_top', 'max'),
            std_salary_bottom=('salary_bottom', 'std'),
            std_salary_top=('salary_top', 'std'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()
        total_vacancies = len(self._db.select_for_analytics('get_salary_by_role'))
        summary['with_salary'] = summary['count_vacancies'] / total_vacancies

    def analyze_salaries_by_city(self):
        raw_data = self._db.select_for_analytics('get_salary_by_city')

        df = pd.DataFrame(raw_data, columns=['city', 'salary_bottom', 'salary_top'])
        df['salary_bottom'] = pd.to_numeric(df['salary_bottom'], errors='coerce')
        df['salary_top'] = pd.to_numeric(df['salary_top'], errors='coerce')
        df = df.dropna(subset=['salary_bottom', 'salary_top'])

        summary = df.groupby('city').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            min_salary=('salary_bottom', 'min'),
            max_salary=('salary_top', 'max'),
            std_salary_bottom=('salary_bottom', 'std'),
            std_salary_top=('salary_top', 'std'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()