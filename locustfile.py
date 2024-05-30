import os
import requests
import random
from locust import task, HttpUser

BASE_URL = 'http://167.172.172.115:52355'


def get_token_file_path():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    return os.path.join(current_directory, 'token.txt')


def get_token():
    full_token_path = get_token_file_path()

    if os.path.exists(full_token_path):
        with open(full_token_path, 'r') as file:
            existing_token = file.read().strip()
        check_response = requests.get(f'{BASE_URL}/authorize/{existing_token}')
        if check_response.status_code == 200:
            return existing_token
        else:
            os.remove(full_token_path)

    data = {'name': 'new_1_name'}
    response = requests.post(f'{BASE_URL}/authorize', json=data)
    if response.status_code == 200:
        new_token = response.json()['token']
        with open(full_token_path, 'w') as file:
            file.write(new_token)
        return new_token
    else:
        raise Exception(f"Failed to get token: {response.text}")


class PublicationUser(HttpUser):
    token = None
    post_ids = set()

    def on_start(self):
        self.token = get_token()

    @task(7)
    def get_all_meme(self):
        self.client.get('/meme', headers={'Authorization': f'{self.token}'})

    @task(1)
    def create_meme(self):
        payload = {
            "text": "Test 1",
            "url": "https://9gag.com/gag/amoNKdV",
            "tags": ["mosquito", "spray"],
            "info": {"colors": ["red", "white"], "objects": ["picture", "text"]},
        }
        self.client.post('/meme', json=payload, headers={'Authorization': f'{self.token}'})
        self.post_ids.add(random.randrange(1, 50))

    def on_stop(self):
        for post_id in self.post_ids:
            self.client.delete(f'/meme/{post_id}')
