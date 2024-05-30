import requests
import allure
import conftest
from endpoints.bese_endpoints import BaseEndpoint


class DeleteMeme(BaseEndpoint):

    @allure.step("Send DELETE request and validate successful deletion")
    def remove_meme(self, token, meme_id):
        headers = {
            'Authorization': f'{token}'
        }
        self.response = requests.delete(f'{conftest.BASE_URL}/meme/{meme_id}', headers=headers)
        self.status_code = self.response.status_code
