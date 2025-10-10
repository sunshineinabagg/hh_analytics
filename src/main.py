import asyncio
import logging

from nest_asyncio import apply

import httpx

from db_manager.db import Database
from data_collector.collector import Collector

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)

apply()
db = Database()


async def start_collect():
    client = httpx.AsyncClient()
    collector = Collector(client, db)
    await collector.start()
    await client.aclose()


async def main():
    logging.info('Application is running...')
    await db.connect()
    check_db = await db.create_table()
    if check_db is None:
        asyncio.run(start_collect())
    # start_analytics()
    await db.close_connection()
    logging.info('End.')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Something went wrong: {str(e)}')
