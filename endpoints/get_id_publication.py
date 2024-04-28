import requests
import allure
import conftest
from endpoints.bese_endpoints import BaseEndpoint
from endpoints.json_shemas import MemePostPayload


class GetIdPublication(BaseEndpoint):
    response_data = None

    @allure.step("Get meme ID from the publication")
    def get_id_publication(self, token, meme_id):
        headers = {
            'Authorization': f'{token}'
        }
        self.response = requests.get(f'{conftest.BASE_URL}/meme/{meme_id}', headers=headers)
        self.status_code = self.response.status_code
        if self.response.status_code == 200 and self.response.text:
            self.response_data = MemePostPayload(**self.response.json())
        else:
            self.response_data = None

    @allure.step("Check if the ID is correct")
    def check_id_is_correct(self, meme_id):
        if self.response_data is not None:
            assert self.response_data.id == meme_id
