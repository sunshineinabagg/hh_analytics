import json

from src.models.vacancy_model import Vacancy

roles = (156, 160, 10, 12, 150, 25, 165, 34, 36, 73, 155, 96, 164, 104, 157, 107, 112, 113,
         148, 114, 116, 121, 124, 125, 126)


async def skills_check(skills):
    result = ''
    for skill in skills:
        result += skill['name'] + ', '
    if result == '':
        return None
    else:
        return result


async def json_loads(raw_data: str | bytes) -> dict:
    return json.loads(raw_data)


async def formalize_data(data: dict):
    if data.get('errors'):
        return None
    vacancy = Vacancy(id=data['id'],
                      name=data['name'],
                      city=data['address']['city'] if data.get('address') else None,
                      salary_bottom=str(data['salary_range']['from']) + data['salary_range']['currency'] if data.get(
                          'salary_range') else None,
                      salary_top=str(data['salary_range']['to']) + data['salary_range']['currency'] if data.get(
                          'salary_range') else None,
                      published_at=data['published_at'],
                      employer_name=data['employer']['name'],
                      key_skills=await skills_check(data['key_skills']),
                      schedule=data['schedule']['id'],
                      professional_role_id=data['professional_roles'][0]['id'],
                      professional_role=data['professional_roles'][0]['name'],
                      experience=data['experience']['id'])
    return vacancy
