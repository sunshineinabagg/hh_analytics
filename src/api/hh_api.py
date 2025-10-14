import logging
from datetime import date, timedelta
import httpx
import private_settings
from src.utils import json_loads


class HeadHunterApi:
    _API_URL = 'https://api.hh.ru'
    _HH_USER_AGENT = 'hh_analytics/1.0 (sunshineinabagg@yandex.ru)'
    __token = private_settings.TOKEN

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def _send_request(self, method: str, **kwargs):
        response = await self.client.get(url=self._API_URL + method,
                                         headers={'HH-User-Agent': self._HH_USER_AGENT,
                                                  'Authorization': f'Bearer {self.__token}'},
                                         **kwargs)
        if response.status_code != 200:
            logging.info(f'Ошибка: {response.text}\n Код: {response.status_code}')
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
