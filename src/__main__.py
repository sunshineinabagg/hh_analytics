# src/main.py

import asyncio
import logging

from nest_asyncio import apply

# Импорты с префиксом src. — обязательно при запуске через python -m src.main
from src.db_manager.db import Database
from src.analytics.analyzer import Analyzer
from src.analytics.infographics import Infographics

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)

apply()
db = Database()


async def start_collect():
    # Этот блок НЕ выполняется — он закомментирован в main()
    from src.data_collector.collector import Collector
    await db.async_connect()
    check_db = await db.create_table()
    if check_db is None:
        import httpx
        client = httpx.AsyncClient()
        await Collector(client, db).start()
        await client.aclose()
    else:
        logging.info('Database is not empty.')
    await db.async_disconnect()


def start_analytics():
    """Запускает анализ и визуализацию на основе существующей db.sqlite"""
    db.connect()
    analyzer = Analyzer(db)
    infographics = Infographics()
    infographics.generate_all(analyzer)
    db.disconnect()


async def main():
    logging.info('Application is running...')
    # await start_collect()   # ← сбор отключён, используем готовую БД
    start_analytics()
    logging.info('End.')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'Something went wrong: {str(e)}')
