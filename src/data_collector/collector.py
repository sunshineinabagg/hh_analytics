import asyncio
import time
import logging
from httpx import AsyncClient
from src.api.hh_api import HeadHunterApi
from src.db_manager.db import Database
from src.utils import formalize_data


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
        self._roles = None
        self._range = None

    async def _get_last_vacancy(self):
        last_vacancy = await self._hh.get_vacancies()
        return last_vacancy['items'][0]['id']

    async def _set_roles(self):
        all_roles = await self._hh.get_professional_roles()
        self._roles = process_roles(all_roles)
        return self._roles

    async def _set_range(self):
        self._range = int(await self._get_last_vacancy())
        return self._range

    async def _process_vacancy(self, vacancy_id: int, semaphore: asyncio.Semaphore):
        try:
            async with semaphore:
                raw_vacancy = await self._hh.get_vacancy(vacancy_id)
                if not isinstance(raw_vacancy, dict):
                    logging.info(f'Vacancy {vacancy_id} is not found')
                    return
                if raw_vacancy.get('professional_roles'):
                    for role in raw_vacancy['professional_roles']:
                        if role['id'] in self._roles.keys():
                            logging.info(f'Vacancy {vacancy_id} processing has started')
                            vacancy = await formalize_data(raw_vacancy)
                            await self._db.insert_vacancy(vacancy)
                            logging.info(f'Vacancy {vacancy_id} processing completed successfully')
                            return
                logging.info(f'Vacancy {vacancy_id} was skipped')
        except Exception as e:
            logging.warning(f'Error while processing: {str(e)}')
            pass

    async def start(self):
        await self._set_roles()
        await self._set_range()
        tasks = set()
        semaphore = asyncio.Semaphore(10)
        step = 1000
        starting_time = time.time()
        for ceiling in range(self._range, 125796748, -step):
            for vacancy_id in range(ceiling, ceiling - step, -1):
                tasks.add(asyncio.create_task(self._process_vacancy(vacancy_id, semaphore)))
            await asyncio.gather(*tasks)
        logging.info(f"Collector's time spent: {time.time() - starting_time:.3f} sec")
