import pandas as pd

from src.db_manager.db import Database

class Analyzator:
    def __init__(self, db: Database):
        self._db = db

    def analyze_salaries_by_role(self):
        raw_data = self._db.select_for_analytics('get_salary_by_role')

        df = pd.DataFrame(raw_data, columns=['professional_role', 'salary_bottom', 'salary_top', 'currency'])
        for col in ['professional_role', 'currency']:
            df[col] = df[col].str.strip('"')
        df['salary_bottom'] = df['salary_bottom'].str.strip('"').replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].str.strip('"').replace('None', None).astype(float)
        df = df[df['currency'] == 'RUR']
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

        return summary

    def analyze_salaries_by_city(self):
        raw_data = self._db.select_for_analytics('get_salary_by_city')

        df = pd.DataFrame(raw_data, columns=['city', 'salary_bottom', 'salary_top', 'currency'])
        for col in ['city', 'currency']:
            df[col] = df[col].str.strip('"')

        df['city'] = df['city'].replace('None', None)
        df['salary_bottom'] = df['salary_bottom'].str.strip('"').replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].str.strip('"').replace('None', None).astype(float)
        df = df[df['currency'] == 'RUR']

        df = df.dropna(subset=['city', 'salary_bottom', 'salary_top'])

        summary = df.groupby('city').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            min_salary=('salary_bottom', 'min'),
            max_salary=('salary_top', 'max'),
            std_salary_bottom=('salary_bottom', 'std'),
            std_salary_top=('salary_top', 'std'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()

        return summary

    def analyze_roles_count(self):
        raw_data = self._db.select_for_analytics('get_roles_count')

        df = pd.DataFrame(raw_data, columns=['professional_role'])

        summary = df['professional_role'].value_counts().reset_index()
        summary.columns = ['professional_role', 'count_vacancies']

        total_vacancies = summary['count_vacancies'].sum()
        summary['share'] = summary['count_vacancies'] / total_vacancies

        return summary
