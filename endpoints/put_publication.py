import requests
import allure
import conftest
from endpoints.bese_endpoints import BaseEndpoint


class PutPublication(BaseEndpoint):

    @allure.step("Put mem")
    def put_new_publication(self, token, meme_id, payload):
        payload = payload if payload else conftest.PAYLOAD
        headers = {
            'Authorization': f'{token}'
        }
        self.response = requests.put(f'{conftest.BASE_URL}/meme/{meme_id}', headers=headers, json=payload)
        self.status_code = self.response.status_code

    @allure.step("Check text is correct")
    def check_text(self, text):
        assert self.response.json()['text'] == text
