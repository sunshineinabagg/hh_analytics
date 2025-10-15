import pandas as pd

from src.db_manager.db import Database


class Analyzer:
    def __init__(self, db: Database):
        self._db = db

    def full_analysis(self):
        salary_by_role = self.analyze_salaries_by_role()
        salary_by_city = self.analyze_salaries_by_city()
        roles_count = self.analyze_roles_count()
        salaries_by_experience = self.analyze_salaries_by_experience()
        key_skills = self.analyze_key_skills()
        schedule_analysis = self.analyze_schedule()
        vacancy_dynamics = self.analyze_vacancy_dynamics()
        employers_analysis = self.analyze_employers()

        full_results = {
            'salary_by_role': salary_by_role,
            'salary_by_city': salary_by_city,
            'roles_count': roles_count,
            'salaries_by_experience': salaries_by_experience,
            'key_skills': key_skills,
            'schedule_analysis': schedule_analysis,
            'vacancy_dynamics': vacancy_dynamics,
            'employers_analysis': employers_analysis
        }

        return full_results

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

    def analyze_salaries_by_experience(self):
        raw_data = self._db.select_for_analytics('get_salary_by_experience')

        df = pd.DataFrame(raw_data,
                          columns=['experience', 'professional_role', 'salary_bottom', 'salary_top', 'currency'])
        for col in ['experience', 'professional_role', 'currency']:
            df[col] = df[col].str.strip('"')

        df['salary_bottom'] = df['salary_bottom'].str.strip('"').replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].str.strip('"').replace('None', None).astype(float)
        df = df[df['currency'] == 'RUR']
        df = df.dropna(subset=['salary_bottom', 'salary_top'])

        summary = df.groupby(['experience', 'professional_role']).agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            min_salary=('salary_bottom', 'min'),
            max_salary=('salary_top', 'max'),
            std_salary_bottom=('salary_bottom', 'std'),
            std_salary_top=('salary_top', 'std'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()

        return summary

    def analyze_key_skills(self):
        raw_data = self._db.select_for_analytics('get_key_skills')

        df = pd.DataFrame(raw_data, columns=['professional_role', 'key_skills'])
        for col in ['professional_role', 'key_skills']:
            df[col] = df[col].str.strip('"')

        df['key_skills'] = df['key_skills'].str.split(',')
        df = df.explode('key_skills')
        df['key_skills'] = df['key_skills'].str.strip()
        df = df[df['key_skills'] != '']
        df = df[df['key_skills'] != 'None']

        skill_counts = df['key_skills'].value_counts().reset_index()
        skill_counts.columns = ['skill', 'frequency']

        role_skill_counts = df.groupby(['professional_role', 'key_skills']).size().reset_index(name='frequency')

        return {
            'overall': skill_counts,
            'by_role': role_skill_counts
        }

    def analyze_schedule(self):
        raw_data = self._db.select_for_analytics('get_schedule_analysis')

        df = pd.DataFrame(raw_data, columns=['schedule', 'salary_bottom', 'salary_top', 'currency', 'published_at'])
        for col in ['schedule', 'currency']:
            df[col] = df[col].str.strip('"')

        df['salary_bottom'] = df['salary_bottom'].str.strip('"').replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].str.strip('"').replace('None', None).astype(float)
        df = df[df['currency'] == 'RUR']
        df = df.dropna(subset=['salary_bottom', 'salary_top'])

        # 1
        schedule_distribution = df['schedule'].value_counts(normalize=True).reset_index()
        schedule_distribution.columns = ['schedule', 'share']

        # 2
        schedule_salary_summary = df.groupby('schedule').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()

        # 3
        df['published_at'] = df['published_at'].str.strip('"')
        df['published_at'] = pd.to_datetime(df['published_at']).dt.tz_localize(None)

        df['month'] = df['published_at'].dt.to_period('M')
        schedule_trend = df.groupby(['month', 'schedule']).size().reset_index(name='count')

        return {
            'distribution': schedule_distribution,
            'salary_summary': schedule_salary_summary,
            'trend': schedule_trend
        }

    def analyze_vacancy_dynamics(self):
        raw_data = self._db.select_for_analytics('get_vacancy_dynamics')

        df = pd.DataFrame(raw_data,
                          columns=['published_at', 'salary_bottom', 'salary_top', 'currency', 'professional_role'])
        for col in ['currency', 'professional_role']:
            df[col] = df[col].str.strip('"')

        df['published_at'] = df['published_at'].str.strip('"')
        df['published_at'] = pd.to_datetime(df['published_at']).dt.tz_localize(None)
        df['salary_bottom'] = df['salary_bottom'].str.strip('"').replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].str.strip('"').replace('None', None).astype(float)
        df = df[df['currency'] == 'RUR']
        df = df.dropna(subset=['salary_bottom', 'salary_top'])

        df['month'] = df['published_at'].dt.to_period('M')
        monthly_summary = df.groupby('month').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()

        role_monthly_summary = df.groupby(['month', 'professional_role']).size().reset_index(name='count')

        return {
            'monthly_summary': monthly_summary,
            'role_monthly_summary': role_monthly_summary
        }

    def analyze_employers(self):
        raw_data = self._db.select_for_analytics('get_employer_analysis')

        df = pd.DataFrame(raw_data, columns=['employer_name', 'professional_role', 'key_skills',
                                             'salary_bottom', 'salary_top', 'currency'])
        for col in ['employer_name', 'professional_role', 'key_skills', 'currency']:
            df[col] = df[col].str.strip('"')

        df['salary_bottom'] = df['salary_bottom'].str.strip('"').replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].str.strip('"').replace('None', None).astype(float)
        df = df[df['currency'] == 'RUR']
        df_with_salary = df.dropna(subset=['salary_bottom', 'salary_top'])

        # 1. top 10
        top_employers = df['employer_name'].value_counts().reset_index()
        top_employers.columns = ['employer_name', 'vacancy_count']
        top_employers = top_employers.head(10)

        top_employers_list = top_employers['employer_name'].tolist()
        # 2
        employer_salary_summary = df_with_salary.groupby('employer_name').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()

        # 3
        df['key_skills'] = df['key_skills'].str.split(',')
        df = df.explode('key_skills')
        df['key_skills'] = df['key_skills'].str.strip()
        df = df[df['key_skills'] != '']
        df = df[df['key_skills'] != 'None']
        skill_counts_by_employer = (
            df[df['employer_name'].isin(top_employers_list)]
            .groupby(['employer_name', 'key_skills'])
            .size()
            .reset_index(name='frequency')
        )

        return {
            'top_employers': top_employers,
            'employer_salary_summary': employer_salary_summary,
            'skill_counts_by_employer': skill_counts_by_employer
        }
