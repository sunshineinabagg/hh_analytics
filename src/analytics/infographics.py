import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud

from src.analytics.extractor import Extractor

sns.set(style="whitegrid")
plt.rcParams.update({'font.size': 10})

os.makedirs("reports/plots", exist_ok=True)


class Infographics:
    """Класс для визуализации результатов аналитики."""

    def __init__(self, db):
        self.ex = Extractor(db)

    def plot_salary_by_role(self, df: pd.DataFrame):
        """Задача 1: Зарплаты по направлениям"""
        df['avg_salary'] = (df['avg_salary_bottom'] + df['avg_salary_top']) / 2
        top = df.nlargest(15, 'avg_salary')
        plt.figure(figsize=(12, 8))
        sns.barplot(data=top, y='professional_role', x='avg_salary', palette="viridis")
        plt.title("Средняя зарплата по IT-направлениям (ТОП-15)")
        plt.xlabel("Средняя зарплата (RUB)")
        plt.tight_layout()
        plt.savefig("reports/plots/salary_by_role.png")
        plt.close()

    def plot_salary_by_city(self, df: pd.DataFrame):
        """Задача 2: Зарплаты по городам"""
        df['avg_salary'] = (df['avg_salary_bottom'] + df['avg_salary_top']) / 2
        top = df.nlargest(10, 'avg_salary')
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top, y='city', x='avg_salary', palette="magma")
        plt.title("ТОП-10 городов по средней зарплате")
        plt.xlabel("Средняя зарплата (RUB)")
        plt.tight_layout()
        plt.savefig("reports/plots/salary_by_city.png")
        plt.close()

    def plot_roles_count(self, df: pd.DataFrame):
        """Задача 3: Востребованность направлений"""
        top = df.nlargest(15, 'count_vacancies')
        fig, ax = plt.subplots(1, 2, figsize=(16, 6))
        sns.barplot(data=top, y='professional_role', x='count_vacancies', ax=ax[0], palette="Blues_d")
        ax[0].set_title("Количество вакансий по направлениям (ТОП-15)")

        top7 = df.nlargest(7, 'count_vacancies')
        others = pd.DataFrame({
            'professional_role': ['Остальные'],
            'count_vacancies': [df['count_vacancies'].sum() - top7['count_vacancies'].sum()]
        })
        pie_data = pd.concat([top7, others])
        ax[1].pie(pie_data['count_vacancies'], labels=pie_data['professional_role'], autopct='%1.1f%%')
        ax[1].set_title("Доля направлений")
        plt.tight_layout()
        plt.savefig("reports/plots/roles_count.png")
        plt.close()

    def plot_salaries_by_experience(self, df: pd.DataFrame):
        """Задача 4: Опыт vs зарплата"""
        df['avg_salary'] = (df['avg_salary_bottom'] + df['avg_salary_top']) / 2
        exp_order = ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
        df['experience'] = pd.Categorical(df['experience'], categories=exp_order, ordered=True)
        summary = df.groupby('experience', observed=True)['avg_salary'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        sns.barplot(data=summary, x='experience', y='avg_salary', palette="rocket")
        plt.title("Средняя зарплата в зависимости от опыта")
        plt.xlabel("Уровень опыта")
        plt.ylabel("Средняя зарплата (RUB)")
        plt.xticks(ticks=[0,1,2,3], labels=['Нет опыта', '1–3 года', '3–6 лет', 'Более 6 лет'])
        plt.tight_layout()
        plt.savefig("reports/plots/salaries_by_experience.png")
        plt.close()

    def plot_key_skills(self, skill_data: dict):
        """Задача 5: Навыки"""
        overall = skill_data['overall'].head(20)
        plt.figure(figsize=(12, 8))
        sns.barplot(data=overall, y='skill', x='frequency', palette="cividis")
        plt.title("ТОП-20 самых востребованных навыков")
        plt.xlabel("Частота упоминания")
        plt.tight_layout()
        plt.savefig("reports/plots/key_skills_bar.png")
        plt.close()

        word_freq = dict(zip(overall['skill'], overall['frequency']))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.title("Облако популярных навыков")
        plt.tight_layout()
        plt.savefig("reports/plots/key_skills_wordcloud.png")
        plt.close()

    def plot_schedule_analysis(self, schedule_data: dict):
        """Задача 6: График работы"""
        dist = schedule_data['distribution']
        salary = schedule_data['salary_summary']

        labels_map = {
            'fullDay': 'Полный день',
            'remote': 'Удалёнка',
            'flexible': 'Гибкий',
            'shift': 'Сменный',
            'flyInFlyOut': 'Вахта'
        }

        dist['label'] = dist['schedule'].map(labels_map).fillna(dist['schedule'])
        plt.figure(figsize=(8, 8))
        plt.pie(dist['share'], labels=dist['label'], autopct='%1.1f%%')
        plt.title("Доля форматов работы")
        plt.tight_layout()
        plt.savefig("reports/plots/schedule_pie.png")
        plt.close()

        salary['avg_salary'] = (salary['avg_salary_bottom'] + salary['avg_salary_top']) / 2
        salary['label'] = salary['schedule'].map(labels_map).fillna(salary['schedule'])
        plt.figure(figsize=(10, 5))
        sns.barplot(data=salary, x='label', y='avg_salary', palette="Spectral")
        plt.title("Средняя зарплата по типу графика")
        plt.xlabel("")
        plt.ylabel("Средняя зарплата (RUB)")
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.savefig("reports/plots/schedule_salary.png")
        plt.close()

    def plot_vacancy_dynamics(self, dynamics: dict):
        """Задача 7: Динамика публикаций"""
        monthly = dynamics['monthly_summary']
        monthly['month'] = monthly['month'].astype(str)
        plt.figure(figsize=(12, 6))
        ax1 = sns.lineplot(data=monthly, x='month', y='count_vacancies', color='blue', marker='o')
        ax1.set_ylabel("Количество вакансий", color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax2 = ax1.twinx()
        sns.lineplot(data=monthly, x='month', y='avg_salary_bottom', color='red', marker='s', ax=ax2)
        ax2.set_ylabel("Средняя зарплата (RUB)", color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        plt.title("Динамика вакансий и зарплат по месяцам")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("reports/plots/vacancy_dynamics.png")
        plt.close()

    def plot_employers_analysis(self, employers: dict):
        """Задача 8: Работодатели"""
        top = employers['top_employers']
        plt.figure(figsize=(10, 8))
        sns.barplot(data=top, y='employer_name', x='vacancy_count', palette="crest")
        plt.title("ТОП-10 работодателей по числу вакансий")
        plt.xlabel("Количество вакансий")
        plt.tight_layout()
        plt.savefig("reports/plots/top_employers.png")
        plt.close()

    def generate_all(self):
        """
        Генерирует все графики, используя методы Analyzer.
        Вызывает каждый метод аналитики и передаёт результат в визуализацию.
        """
        self.plot_salary_by_role(self.ex.analyze_salaries_by_role())
        self.plot_salary_by_city(self.ex.analyze_salaries_by_city())
        self.plot_roles_count(self.ex.analyze_roles_count())
        self.plot_salaries_by_experience(self.ex.analyze_salaries_by_experience())
        self.plot_key_skills(self.ex.analyze_key_skills())
        # self.plot_schedule_analysis(self.ex.analyze_schedule())
        # self.plot_vacancy_dynamics(self.ex.analyze_vacancy_dynamics())
        # self.plot_employers_analysis(self.ex.analyze_employers())
        print("✅ Все графики сохранены в reports/plots/")
