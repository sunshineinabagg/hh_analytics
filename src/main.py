import asyncio
from nest_asyncio import apply

import httpx

from db_manager.db import Database
from data_collector.utils import formalize_data, roles
from data_collector.hh_api import HeadHunterApi
from models.vacancy_model import Vacancy

apply()
db = Database()


async def start_collect():
    client = httpx.AsyncClient()
    hh = HeadHunterApi(client)
    for i in range(125139540, 125137540, -1):
        result = await hh.get_vacancy(i)
        formatted_data: Vacancy = await formalize_data(result.text)
        if formatted_data is None:
            print('Mimo')
        else:
            print('Cur vacancy is ' + formatted_data.id)
            if formatted_data.professional_role_id in roles:
                await db.insert_vacancy(formatted_data)
    await client.aclose()


async def main():
    await db.connect()
    check_db = await db.create_table()
    if not check_db:
        asyncio.run(start_collect())
    db.connect().close()


if __name__ == '__main__':
    asyncio.run(main())
