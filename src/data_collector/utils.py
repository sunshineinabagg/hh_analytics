import json

from src.models.vacancy_model import Vacancy

roles = (156, 160, 10, 12, 150, 25, 165, 34, 36, 73, 155, 96, 164, 104, 157, 107, 112, 113,
         148, 114, 116, 121, 124, 125, 126)


def skills_check(skills):
    result = ''
    for skill in skills:
        result += skill['name'] + ', '
    if result == '':
        return None
    else:
        return result


async def formalize_data(data: str):
    obj: dict = json.loads(data)
    if obj.get('errors'):
        return None
    vacancy = Vacancy(id=obj['id'],
                      name=obj['name'],
                      city=obj['address']['city'] if obj.get('address') else None,
                      salary_bottom=str(obj['salary_range']['from']) + obj['salary_range']['currency'] if obj.get(
                          'salary_range') else None,
                      salary_top=str(obj['salary_range']['to']) + obj['salary_range']['currency'] if obj.get(
                          'salary_range') else None,
                      published_at=obj['published_at'],
                      employer_name=obj['employer']['name'],
                      key_skills=skills_check(obj['key_skills']),
                      schedule=obj['schedule']['id'],
                      professional_role_id=obj['professional_roles'][0]['id'],
                      professional_role=obj['professional_roles'][0]['name'],
                      experience=obj['experience']['id'])
    return vacancy
