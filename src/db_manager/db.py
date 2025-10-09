import aiosqlite

from src.db_manager.settings import DB_NAME
from src.db_manager.statements import Statements


class Database:
    def __init__(self):
        self._db_name = DB_NAME
        self._conn: aiosqlite.Connection | None = None

    async def connect(self):
        if self._conn is None:
            self._conn = await aiosqlite.connect(self._db_name)

    async def close_connection(self):
        await self._conn.close()

    async def create_table(self):
        async with self._conn.cursor() as cursor:
            await cursor.execute(Statements.create_table())
        await self._conn.commit()
        return await self.check_table()

    async def check_table(self):
        async with self._conn.execute(Statements.check_table()) as cursor:
            result = await cursor.fetchone()
        return result

    async def insert_vacancy(self, vacancy):
        async with self._conn.cursor() as cursor:
            statement = Statements.insert_vacancy()
            await cursor.execute(statement,
                                 (vacancy.id,
                                  f'"{vacancy.name}"',
                                  f'"{vacancy.city}"',
                                  f'"{vacancy.salary_bottom}"',
                                  f'"{vacancy.salary_top}"',
                                  f'"{vacancy.published_at}"',
                                  f'"{vacancy.employer_name}"',
                                  f'"{vacancy.key_skills}"',
                                  f'"{vacancy.schedule}"',
                                  f'"{vacancy.professional_role}"',
                                  f'"{vacancy.experience}"'))
        await self._conn.commit()
