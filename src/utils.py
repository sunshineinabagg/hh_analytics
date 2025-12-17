import json
import logging

from src.models.vacancy_model import Vacancy


async def json_loads(raw_data: str | bytes) -> dict:
    return json.loads(raw_data)


async def skills_check(skills):
    result = ''
    for skill in skills:
        result += skill['name'] + ', '
    if result == '':
        return None
    else:
        return result


async def formalize_data(data: dict):
    try:
        if data.get('errors'):
            return None
        vacancy = Vacancy(id=data['id'],
                          name=data['name'],
                          city=data['address']['city'] if data.get('address') else None,
                          salary_bottom=data['salary_range']['from'] if data.get('salary_range') else None,
                          salary_top=data['salary_range']['to'] if data.get('salary_range') else None,
                          currency=data['salary_range']['currency'] if data.get('salary_range') else None,
                          published_at=data['published_at'],
                          employer_name=data['employer']['name'],
                          key_skills=await skills_check(data['key_skills']),
                          schedule=data['schedule']['id'],
                          professional_role_id=data['professional_roles'][0]['id'],
                          professional_role=data['professional_roles'][0]['name'],
                          experience=data['experience']['id'])
        return vacancy
    except Exception as e:
        logging.warning(f'Formalizing error {e} with data {data}')
        pass
