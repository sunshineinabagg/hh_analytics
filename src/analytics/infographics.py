# src/analytics/infographics.py

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from wordcloud import WordCloud

# === Профессиональный стиль ===
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.titlesize': 13,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False
})

sns.set_palette("Set2")


def _ensure_dir():
    """Создаёт директорию для сохранения графиков, если её нет."""
    os.makedirs("reports/plots", exist_ok=True)


def _format_count(n):
    """Форматирует число с пробелами: 1234 → '1 234'"""
    return f"{int(n):,}".replace(",", " ")


# === ЗАДАЧА 1: Медианная зарплата по ролям ===
def plot_salary_by_role(df: pd.DataFrame):
    df['median_salary'] = (df['median_salary_bottom'] + df['median_salary_top']) / 2
    df = df.sort_values('median_salary', ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(df['professional_role'], df['median_salary'], color=sns.color_palette("viridis", len(df)))
    for i, (role, sal, cnt) in enumerate(zip(df['professional_role'], df['median_salary'], df['count_vacancies'])):
        ax.text(sal + max(df['median_salary']) * 0.01, i, f"{_format_count(sal)} ₽", va='center', fontsize=9)
    ax.set_title("Медианная зарплата по IT-направлениям (ТОП-15)\n"
                 f"(всего вакансий в выборке: {_format_count(df['count_vacancies'].sum())})",
                 fontsize=12, pad=20)
    ax.set_xlabel("Медианная зарплата (RUB)")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig("reports/plots/salary_by_role.png")
    plt.close()


# === ЗАДАЧА 2: Города ===
def plot_salary_by_city(df: pd.DataFrame):
    df['median_salary'] = (df['median_salary_bottom'] + df['median_salary_top']) / 2
    df = df.sort_values('median_salary', ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(df['city'], df['median_salary'], color=sns.color_palette("magma", len(df)))
    for i, (city, sal, cnt) in enumerate(zip(df['city'], df['median_salary'], df['count_vacancies'])):
        ax.text(sal + max(df['median_salary']) * 0.01, i, f"{_format_count(sal)} ₽", va='center', fontsize=9)
    ax.set_title("ТОП-10 городов по медианной зарплате\n"
                 f"(всего вакансий: {_format_count(df['count_vacancies'].sum())})",
                 fontsize=12, pad=15)
    ax.set_xlabel("Медианная зарплата (RUB)")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig("reports/plots/salary_by_city.png")
    plt.close()


# === ЗАДАЧА 3: Популярность ролей ===
def plot_roles_count(df: pd.DataFrame):
    df = df.sort_values('count_vacancies', ascending=False)
    top = df.head(15)
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(top['professional_role'], top['count_vacancies'], color=sns.color_palette("Blues", len(top)))
    total = df['count_vacancies'].sum()
    for i, (role, cnt) in enumerate(zip(top['professional_role'], top['count_vacancies'])):
        pct = cnt / total * 100
        ax.text(cnt + max(top['count_vacancies']) * 0.01, i,
                f"{_format_count(cnt)} ({pct:.1f}%)", va='center', fontsize=9)
    ax.set_title(f"Количество вакансий по направлениям (ТОП-15)\n"
                 f"(всего: {_format_count(total)} вакансий)",
                 fontsize=12, pad=20)
    ax.set_xlabel("Количество вакансий")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig("reports/plots/roles_count.png")
    plt.close()

    # Pie chart
    top7 = df.head(7)
    others = pd.DataFrame({
        'professional_role': ['Остальные'],
        'count_vacancies': [total - top7['count_vacancies'].sum()]
    })
    pie_data = pd.concat([top7, others])
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        pie_data['count_vacancies'],
        labels=pie_data['professional_role'],
        autopct=lambda pct: f"{pct:.1f}%\n({_format_count(pct/100*total)})"
    )
    ax.set_title("Доля направлений в общей выборке", fontsize=12, pad=20)
    plt.tight_layout()
    plt.savefig("reports/plots/roles_pie.png")
    plt.close()


# === ЗАДАЧА 4: Опыт ===
def plot_salaries_by_experience(df: pd.DataFrame):
    df['median_salary'] = (df['median_salary_bottom'] + df['median_salary_top']) / 2
    exp_order = ['noExperience', 'between1And3', 'between3And6', 'moreThan6']
    df['experience'] = pd.Categorical(df['experience'], categories=exp_order, ordered=True)
    grouped = df.groupby('experience', observed=False).agg(
        median_salary=('median_salary', 'mean'),
        total_count=('count_vacancies', 'sum')
    ).reset_index()
    exp_labels = ['Нет опыта', '1–3 года', '3–6 лет', 'Более 6 лет']
    grouped['label'] = exp_labels
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(grouped['label'], grouped['median_salary'], color=sns.color_palette("rocket", 4))
    for i, (label, sal, cnt) in enumerate(zip(grouped['label'], grouped['median_salary'], grouped['total_count'])):
        ax.text(i, sal + max(grouped['median_salary']) * 0.02, f"{_format_count(sal)} ₽", ha='center', fontsize=9)
        ax.text(i, -max(grouped['median_salary']) * 0.1, f"{_format_count(cnt)}", ha='center', fontsize=8, color='gray')
    ax.set_title("Медианная зарплата в зависимости от опыта", fontsize=12, pad=15)
    ax.set_ylabel("Медианная зарплата (RUB)")
    ax.set_xlabel("Уровень опыта")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("reports/plots/salaries_by_experience.png")
    plt.close()


# === ЗАДАЧА 5: Навыки ===
def plot_key_skills(skill_dict: dict):
    overall = skill_dict['overall'].head(20)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(overall['skill'], overall['frequency'], color=sns.color_palette("cividis", len(overall)))
    ax.set_title(f"ТОП-20 самых востребованных навыков\n"
                 f"(всего упоминаний: {_format_count(overall['frequency'].sum())})",
                 fontsize=12, pad=15)
    ax.set_xlabel("Количество упоминаний")
    ax.set_ylabel("Навык")
    plt.tight_layout()
    plt.savefig("reports/plots/key_skills_bar.png")
    plt.close()

    word_freq = dict(zip(overall['skill'], overall['frequency']))
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Облако популярных навыков", fontsize=12, pad=20)
    plt.tight_layout()
    plt.savefig("reports/plots/key_skills_wordcloud.png", dpi=300, bbox_inches='tight')
    plt.close()


# === ЗАДАЧА 6: График работы ===
def plot_schedule_analysis(schedule_dict: dict):
    shares = schedule_dict['schedule_shares']
    label_map = {
        'fullDay': 'Полный день',
        'remote': 'Удалёнка',
        'flexible': 'Гибкий',
        'shift': 'Сменный',
        'flyInFlyOut': 'Вахта'
    }
    shares['label'] = shares['schedule'].map(label_map).fillna(shares['schedule'])
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        shares['total_vacancies'],
        labels=shares['label'],
        autopct=lambda pct: f"{pct:.1f}%\n({_format_count(pct/100 * shares['total_vacancies'].sum())})"
    )
    ax.set_title("Доля форматов работы", fontsize=12, pad=20)
    plt.tight_layout()
    plt.savefig("reports/plots/schedule_shares.png")
    plt.close()


# === ЗАДАЧА 7: Динамика ===
def plot_vacancy_dynamics(dynamics_dict: dict):
    monthly = dynamics_dict['monthly_summary'].copy()
    monthly['month'] = monthly['month'].astype(str)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    color = 'tab:blue'
    ax1.set_xlabel('Месяц')
    ax1.set_ylabel('Количество вакансий', color=color)
    sns.lineplot(data=monthly, x='month', y='count_vacancies', ax=ax1, color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.tick_params(axis='x', rotation=45)
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Средняя зарплата (RUB)', color=color)
    sns.lineplot(data=monthly, x='month', y='avg_salary_bottom', ax=ax2, color=color, marker='s')
    ax2.tick_params(axis='y', labelcolor=color)
    plt.title("Динамика вакансий и зарплат по месяцам", fontsize=12, pad=15)
    plt.tight_layout()
    plt.savefig("reports/plots/vacancy_dynamics.png")
    plt.close()


# === ЗАДАЧА 8: Работодатели ===
def plot_employers_analysis(employers_dict: dict):
    top = employers_dict['top_employers']
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(top['employer_name'], top['vacancy_count'], color=sns.color_palette("crest", len(top)))
    total = top['vacancy_count'].sum()
    for i, (name, cnt) in enumerate(zip(top['employer_name'], top['vacancy_count'])):
        pct = cnt / total * 100
        ax.text(cnt + max(top['vacancy_count']) * 0.01, i,
                f"{_format_count(cnt)} ({pct:.1f}%)", va='center', fontsize=9)
    ax.set_title(f"ТОП-10 работодателей по числу вакансий\n(всего: {_format_count(total)})", fontsize=12, pad=15)
    ax.set_xlabel("Количество вакансий")
    ax.set_ylabel("Компания")
    plt.tight_layout()
    plt.savefig("reports/plots/top_employers.png")
    plt.close()


def generate_all_plots(results: dict):
    """Генерирует все графики по результатам анализа."""
    _ensure_dir()
    plot_salary_by_role(results['salary_by_role'])
    plot_salary_by_city(results['salary_by_city'])
    plot_roles_count(results['roles_count'])
    plot_salaries_by_experience(results['salaries_by_experience'])
    plot_key_skills(results['key_skills'])
    plot_schedule_analysis(results['schedule_analysis'])
    plot_vacancy_dynamics(results['vacancy_dynamics'])
    plot_employers_analysis(results['employers_analysis'])
    print("✅ Все графики сохранены в reports/plots/ (в высоком DPI, с медианой и количеством)")
