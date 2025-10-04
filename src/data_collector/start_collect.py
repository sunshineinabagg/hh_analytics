import httpx
import asyncio

from hh_api import HeadHunterApi


async def start_collect():
    client = httpx.AsyncClient()
    hh = HeadHunterApi(client)
    result = await hh.get_vacancies(page=10)
    print(result.text)
    await client.aclose()


if __name__ == '__main__':
    asyncio.run(start_collect())
