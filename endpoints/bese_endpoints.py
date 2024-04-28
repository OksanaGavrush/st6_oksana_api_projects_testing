import allure


class BaseEndpoint:
    response = None
    status_code = None
    meme_id = None

    @allure.step("Check that the response status code is 200")
    def check_response_is_200(self):
        assert self.response.status_code == 200

    @allure.step("Check that the response status code is 401")
    def check_response_is_401(self):
        assert self.response.status_code == 401, 'UNAUTHORIZED'

    @allure.step("Check that the response status code is 400")
    def check_response_is_400(self):
        assert self.response.status_code == 400

    @allure.step("Verify deletion")
    def check_response_is_404(self):
        assert self.response.status_code == 404

    def check_expected_status(self, response, expected_status):
        assert response.status_code == expected_status

