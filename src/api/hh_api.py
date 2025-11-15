import asyncio
import logging
from datetime import date, timedelta
import httpx
import private_settings
from utils import json_loads


class HeadHunterApi:
    _API_URL = 'https://api.hh.ru'
    _HH_USER_AGENT = 'hh_analytics/1.0 (sunshineinabagg@yandex.ru)'
    __token = private_settings.TOKEN

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _send_request(self, method: str, **kwargs):
        for attempt in (1, 2, 3):
            response: httpx.Response = await self.__send_request(method=method, **kwargs)
            if response.status_code == 429:
                logging.info(f'Request {response.url} has caught code 429. That was {attempt} attempt')
                await asyncio.sleep(attempt)
            else:
                return await json_loads(response.text)

    async def __send_request(self, method: str, **kwargs):
        response = await self.client.get(url=self._API_URL + method,
                                         headers={'HH-User-Agent': self._HH_USER_AGENT,
                                                  'Authorization': f'Bearer {self.__token}'},
                                         **kwargs)
        return response

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
