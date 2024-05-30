import requests
import allure
import conftest
from endpoints.bese_endpoints import BaseEndpoint
import json


class CreateMeme(BaseEndpoint):

    @allure.step("Create mem")
    def create_new_meme(self, token, payload=None):
        payload = payload if payload else conftest.PAYLOAD
        headers = {
            'Authorization': f'{token}'
        }

        self.response = requests.post(f'{conftest.BASE_URL}/meme', headers=headers, json=payload)
        self.status_code = self.response.status_code
        try:
            self.meme_id = self.response.json()['id']
        except json.JSONDecodeError:
            self.meme_id = None
