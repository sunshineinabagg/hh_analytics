import httpx

from settings import (
    API_URL, HH_USER_AGENT)


class HeadHunterApi:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
        # self._token = OauthToken

    async def _send_request(self, method: str, **kwargs):
        response = await self.client.get(url=API_URL+method,
                                         headers={'HH-User-Agent': HH_USER_AGENT})
                                                  # 'Authorization': f'Bearer {self._token}'})
        return response

    async def get_vacancies(self):
        response = await self._send_request(
            method='/vacancies'
        )
        return response

    async def get_vacancy(self, vacancy_id: int):
        response = await self._send_request(
            method=f'/vacancies/{vacancy_id}'
        )
        return response

