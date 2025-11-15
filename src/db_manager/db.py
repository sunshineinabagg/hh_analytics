import logging

import aiosqlite
import sqlite3

from db_manager.statements import CollectorStatements, AnalyticStatements


class Database:
    def __init__(self):
        self._db_name = 'db.sqlite'
        self._conn: aiosqlite.Connection | sqlite3.Connection | None = None

    def connect(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_name)

    def disconnect(self):
        self._conn.close()
        self._conn = None

    async def async_connect(self):
        if self._conn is None:
            self._conn = await aiosqlite.connect(self._db_name)

    async def async_disconnect(self):
        await self._conn.close()
        self._conn = None

    async def create_table(self):
        async with self._conn.cursor() as cursor:
            await cursor.execute(CollectorStatements.create_table())
        await self._conn.commit()
        return await self.check_table()

    async def check_table(self):
        async with self._conn.execute(CollectorStatements.check_table()) as cursor:
            result = await cursor.fetchone()
        return result

    async def insert_vacancy(self, vacancy):
        try:
            async with self._conn.cursor() as cursor:
                statement = CollectorStatements.insert_vacancy()
                await cursor.execute(statement,
                                     (vacancy.id,
                                      f'"{vacancy.name}"',
                                      f'"{vacancy.city}"',
                                      f'"{vacancy.salary_bottom}"',
                                      f'"{vacancy.salary_top}"',
                                      f'"{vacancy.currency}"',
                                      f'"{vacancy.published_at}"',
                                      f'"{vacancy.employer_name}"',
                                      f'"{vacancy.key_skills}"',
                                      f'"{vacancy.schedule}"',
                                      f'"{vacancy.professional_role}"',
                                      f'"{vacancy.experience}"'))
                await self._conn.commit()
        except Exception as e:
            logging.warning(f'Error while insert: {str(e)}')

    def select_for_analytics(self, statement):
        cursor = self._conn.cursor()
        cursor.execute(
            AnalyticStatements.choose_statement(statement)
        )
        return cursor.fetchall()
