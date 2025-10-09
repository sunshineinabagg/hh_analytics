import logging
from httpx import AsyncClient
from src.api.hh_api import HeadHunterApi
from src.db_manager.db import Database
from src.data_collector.utils import formalize_data


def process_roles(cluster):
    for subcluster in cluster['categories']:
        if subcluster['name'] == 'Информационные технологии':
            roles = {role['id']: role['name'] for role in subcluster['roles']}
            return roles
        else:
            continue
    return


class Collector:
    def __init__(self, client: AsyncClient, db: Database):
        self._hh = HeadHunterApi(
            client
        )
        self._db = db
        self.roles = None
        self.range = None

    async def _get_last_vacancy(self):
        last_vacancy = await self._hh.get_vacancies()
        return last_vacancy['items'][0]['id']

    async def _set_roles(self):
        all_roles = await self._hh.get_professional_roles()
        self.roles = process_roles(all_roles)
        return self.roles

    async def _set_range(self):
        self.range = int(await self._get_last_vacancy())
        return self.range

    async def _process_vacancy(self, vacancy_id: int):
        raw_vacancy = await self._hh.get_vacancy(vacancy_id)
        if raw_vacancy.get('professional_roles'):
            for role in raw_vacancy['professional_roles']:
                if role['id'] in self.roles.keys():
                    logging.info(f'Vacancy {raw_vacancy["id"]} processing has started')
                    vacancy = await formalize_data(raw_vacancy)
                    await self._db.insert_vacancy(vacancy)
                    logging.info(f'Vacancy {raw_vacancy["id"]} processing completed successfully')
                    return
                else:
                    logging.info(f'Vacancy {raw_vacancy["id"]} was skipped')

    async def start(self):
        await self._set_roles()
        await self._set_range()

        for vacancy_id in range(self.range, self.range - 10000, -1):
            await self._process_vacancy(vacancy_id)
