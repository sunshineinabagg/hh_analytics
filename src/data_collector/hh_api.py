import json

import httpx

from src.data_collector.settings import (
    API_URL, HH_USER_AGENT, token)


class HeadHunterApi:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        self._token = token

    async def _send_request(self, method: str, **kwargs):
        response = await self.client.get(url=API_URL+method,
                                         headers={'HH-User-Agent': HH_USER_AGENT,
                                                  'Authorization': f'Bearer {self._token}'},
                                         **kwargs)
        return response

    async def get_vacancies(self, page: int = 0, per_page: int = 1):
        response = await self._send_request(
            method=f'/vacancies?page={page}&per_page={per_page}'
        )
        return response

    async def get_vacancy(self, vacancy_id: int):
        response = await self._send_request(
            method=f'/vacancies/{vacancy_id}'
        )
        return response
