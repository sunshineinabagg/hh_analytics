import asyncio
import logging

from nest_asyncio import apply

import httpx

from db_manager.db import Database
from data_collector.collector import Collector
from analytics.extractor import Extractor

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)

apply()
db = Database()


async def start_collect():
    await db.async_connect()
    check_db = await db.create_table()
    if check_db is None:
        client = httpx.AsyncClient()
        await Collector(client, db).start()
        await client.aclose()
    else:
        logging.info('Database is not empty.')
    await db.async_disconnect()


def start_analytics():
    db.connect()
    Extractor(db).full_analysis()
    db.disconnect()


async def main():
    logging.info('Application is running...')
    await start_collect()
    # start_analytics()
    logging.info('End.')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logging.warning(f'Something went wrong: {str(e)}')
