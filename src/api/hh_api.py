from datetime import date, timedelta
import httpx

from src.data_collector.settings import (
    API_URL, HH_USER_AGENT, token)
from src.data_collector.utils import json_loads


class HeadHunterApi:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self._token = token

    async def _send_request(self, method: str, **kwargs):
        response = await self.client.get(url=API_URL+method,
                                         headers={'HH-User-Agent': HH_USER_AGENT,
                                                  'Authorization': f'Bearer {self._token}'},
                                         **kwargs)
        return await json_loads(response.text)

    async def get_professional_roles(self):
        response = await self._send_request(
            method='/professional_roles'
        )
        return response

    async def get_vacancies(self):
        response = await self._send_request(
            method=f'/vacancies?per_page=1&date_from={str(date.today() - timedelta(days=1))}'
        )
        return response

    async def get_vacancy(self, vacancy_id: int):
        response = await self._send_request(
            method=f'/vacancies/{vacancy_id}'
        )
        return response
