import pandas as pd

from db_manager.db import Database


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
        """
        Задача 1 1. Анализ уровня заработных плат по направлениям (`professional_role`)
        :return:
        pd.DataFrame: DataFrame, содержащий статистику зарплат, сгруппированную по профессиональным ролям,
                      включая долю вакансий с указанными зарплатами.
        """
        raw_data = self._db.select_for_analytics('get_salary_by_role')

        df = pd.DataFrame(raw_data, columns=['professional_role', 'salary_bottom', 'salary_top', 'currency',
                                             'total_vacancies'])
        for col in ['professional_role', 'salary_bottom', 'salary_top', 'currency']:
            df[col] = df[col].str.strip('"')
        df['salary_bottom'] = df['salary_bottom'].astype(float)
        df['salary_top'] = df['salary_top'].astype(float)

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

        summary = summary.merge(df[['professional_role', 'total_vacancies']].drop_duplicates(), on='professional_role',
                                how='left')
        summary['with_salary'] = summary['count_vacancies'] / summary['total_vacancies']

        return summary

    def analyze_salaries_by_city(self):
        """
        Задача 2. Анализ зарплатных ожиданий по городам (`city`)
        :return:
        pd.DataFrame: DataFrame, содержащий статистику зарплат, сгруппированную по городам,
                      включая долю вакансий с указанными зарплатами.
        """
        raw_data = self._db.select_for_analytics('get_salary_by_city')

        df = pd.DataFrame(raw_data, columns=['city', 'salary_bottom', 'salary_top', 'currency', 'total_vacancies'])
        for col in ['city', 'salary_bottom', 'salary_top', 'currency']:
            df[col] = df[col].str.strip('"')

        df['salary_bottom'] = df['salary_bottom'].astype(float)
        df['salary_top'] = df['salary_top'].astype(float)

        summary = df.groupby('city').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            min_salary=('salary_bottom', 'min'),
            max_salary=('salary_top', 'max'),
            std_salary_bottom=('salary_bottom', 'std'),
            std_salary_top=('salary_top', 'std'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()

        summary = summary.merge(df[['city', 'total_vacancies']].drop_duplicates(), on='city', how='left')

        summary['with_salary'] = summary['count_vacancies'] / summary['total_vacancies']

        return summary

    def analyze_roles_count(self):
        """
        Задача 3. Анализ востребованности направлений (`professional_role`)
        :return:
        pd.DataFrame: DataFrame, содержащий количество и долю вакансий, сгруппированных по профессиональным ролям.
        """
        raw_data = self._db.select_for_analytics('get_roles_count')

        df = pd.DataFrame(raw_data, columns=['professional_role', 'count_vacancies'])
        for col in ['professional_role']:
            df[col] = df[col].str.strip('"')

        total_vacancies = df['count_vacancies'].sum()
        df['share'] = df['count_vacancies'] / total_vacancies

        return df

    def analyze_salaries_by_experience(self):
        """
        Задача 4. Анализ опыта работы (`experience`) и его влияния на зарплату
        :return:
        pd.DataFrame: DataFrame, содержащий статистику зарплат, сгруппированную по категориям опыта
                      и профессиональным ролям, включая общее количество вакансий и вакансии с указанными зарплатами.
        """
        raw_data = self._db.select_for_analytics('get_salary_by_experience')

        df = pd.DataFrame(raw_data,
                          columns=['experience', 'professional_role', 'salary_bottom', 'salary_top', 'currency',
                                   'total_vacancies'])
        for col in ['experience', 'professional_role', 'salary_bottom', 'salary_top', 'currency']:
            df[col] = df[col].str.strip('"')

        df['salary_bottom'] = df['salary_bottom'].astype(float)
        df['salary_top'] = df['salary_top'].astype(float)

        summary = df.groupby(['experience', 'professional_role']).agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            min_salary=('salary_bottom', 'min'),
            max_salary=('salary_top', 'max'),
            std_salary_bottom=('salary_bottom', 'std'),
            std_salary_top=('salary_top', 'std'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()

        summary = summary.merge(df[['experience', 'professional_role', 'total_vacancies']].drop_duplicates(),
                                on=['experience', 'professional_role'], how='left')

        return summary

    def analyze_key_skills(self):
        """
        Задача 5. Анализ популярных навыков (`key_skills`)
        :return:
        dict: Словарь, содержащий:
            - overall: DataFrame с частотой встречаемости ключевых навыков.
            - by_role: DataFrame с частотой встречаемости ключевых навыков по профессиональным ролям.
        """
        raw_data = self._db.select_for_analytics('get_key_skills')

        df = pd.DataFrame(raw_data, columns=['professional_role', 'key_skills'])
        for col in ['professional_role', 'key_skills']:
            df[col] = df[col].str.strip('"')

        df['key_skills'] = df['key_skills'].str.split(',')
        df = df.explode('key_skills')
        df['key_skills'] = df['key_skills'].str.strip()
        df = df[df['key_skills'] != '']

        skill_counts = df['key_skills'].value_counts().reset_index()
        skill_counts.columns = ['skill', 'frequency']

        role_skill_counts = df.groupby(['professional_role', 'key_skills']).size().reset_index(name='frequency')

        return {
            'overall': skill_counts,
            'by_role': role_skill_counts
        }

    def analyze_schedule(self):
        """
        Задача 6. Анализ типов графика работы (`schedule`)
        :return:
        dict: Словарь, содержащий:
            - schedule_shares: DataFrame с долей каждого типа графика работы.
            - avg_salary_by_schedule: DataFrame со средними зарплатами по типам графика работы.
            - schedule_dynamics: DataFrame с динамикой популярности типов графика работы по месяцам.
        """
        raw_data = self._db.select_for_analytics('get_schedule_analysis')

        df = pd.DataFrame(raw_data, columns=['schedule', 'salary_bottom', 'salary_top', 'currency',
                                             'published_at', 'total_vacancies'])
        for col in ['schedule', 'salary_bottom', 'salary_top', 'currency', 'published_at']:
            df[col] = df[col].str.strip('"')

        df['salary_bottom'] = df['salary_bottom'].replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].replace('None', None).astype(float)
        df['published_at'] = pd.to_datetime(df['published_at']).dt.tz_localize(None)

        # 1
        schedule_shares = (
            df.groupby('schedule')['total_vacancies']
            .first()
            .reset_index()
        )
        total_vacancies = schedule_shares['total_vacancies'].sum()
        schedule_shares['share'] = schedule_shares['total_vacancies'] / total_vacancies

        # 2
        df_with_salary = df.dropna(subset=['salary_bottom', 'salary_top'])
        df_with_salary = df_with_salary[df_with_salary['currency'] == 'RUR']
        avg_salary_by_schedule = df_with_salary.groupby('schedule').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean')
        ).reset_index()

        # 3
        df['month'] = df['published_at'].dt.to_period('M')
        schedule_dynamics = (
            df.groupby(['month', 'schedule'])
            .size()
            .reset_index(name='count')
        )
        return {
            'schedule_shares': schedule_shares,
            'avg_salary_by_schedule': avg_salary_by_schedule,
            'schedule_dynamics': schedule_dynamics
        }

    def analyze_vacancy_dynamics(self):
        """
        Задача 7. Динамика публикации вакансий (`published_at`)
        :return:
        dict: Словарь, содержащий:
            - monthly_summary: DataFrame с ежемесячной статистикой (средние зарплаты, количество вакансий).
            - role_monthly_summary: DataFrame с ежемесячной статистикой по ролям.
        """
        raw_data = self._db.select_for_analytics('get_vacancy_dynamics')

        df = pd.DataFrame(raw_data,
                          columns=['published_at', 'salary_bottom', 'salary_top', 'currency',
                                   'professional_role'])
        for col in ['published_at', 'salary_bottom', 'salary_top', 'currency', 'professional_role']:
            df[col] = df[col].str.strip('"')

        df['published_at'] = pd.to_datetime(df['published_at']).dt.tz_localize(None)
        df['salary_bottom'] = df['salary_bottom'].replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].replace('None', None).astype(float)

        df['month'] = df['published_at'].dt.to_period('M')

        role_monthly_summary = df.groupby(['month', 'professional_role']).size().reset_index(name='count')

        df = df[df['currency'] == 'RUR']
        df = df.dropna(subset=['salary_bottom', 'salary_top'])

        monthly_summary = df.groupby('month').agg(
            avg_salary_bottom=('salary_bottom', 'mean'),
            avg_salary_top=('salary_top', 'mean'),
            count_vacancies=('salary_bottom', 'count')
        ).reset_index()

        return {
            'monthly_summary': monthly_summary,
            'role_monthly_summary': role_monthly_summary
        }

    def analyze_employers(self):
        """
        Задача 8. Анализ активности работодателей (`employer_name`)
        :return:
        dict: Словарь, содержащий:
            - top_employers: DataFrame с топ-10 работодателями по количеству вакансий.
            - employer_salary_summary: DataFrame со статистикой зарплат по работодателям.
            - skill_counts_by_employer: DataFrame с частотой встречаемости ключевых навыков,
                                         где компании перечислены через запятую для каждого навыка.
        """
        raw_data = self._db.select_for_analytics('get_employer_analysis')

        df = pd.DataFrame(raw_data, columns=['employer_name', 'professional_role', 'key_skills',
                                             'salary_bottom', 'salary_top', 'currency'])
        for col in ['employer_name', 'professional_role', 'key_skills',
                    'salary_bottom', 'salary_top', 'currency']:
            df[col] = df[col].str.strip('"')

        df['salary_bottom'] = df['salary_bottom'].replace('None', None).astype(float)
        df['salary_top'] = df['salary_top'].replace('None', None).astype(float)
        df_with_salary = df.dropna(subset=['salary_bottom', 'salary_top'])
        df_with_salary = df_with_salary[df_with_salary['currency'] == 'RUR']

        # 1. top 10
        top_employers = df['employer_name'].value_counts().reset_index()
        top_employers.columns = ['employer_name', 'vacancy_count']
        top_employers = top_employers.head(10)
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
            df.groupby('key_skills')['employer_name']
            .agg(
                companies=lambda x: ', '.join(x.unique()),
                frequency='size'
            )
            .reset_index()
        )
        skill_counts_by_employer = skill_counts_by_employer.sort_values(
            by='frequency', ascending=False
        ).reset_index(drop=True)

        return {
            'top_employers': top_employers,
            'employer_salary_summary': employer_salary_summary,
            'skill_counts_by_employer': skill_counts_by_employer
        }
