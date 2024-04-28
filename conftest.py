import os
import pytest
import requests
from endpoints.create_publication import CreatePublication
from endpoints.delete_publication import DeletePublication
from endpoints.get_id_publication import GetIdPublication
from endpoints.put_publication import PutPublication


BASE_URL = 'http://167.172.172.115:52355'

PAYLOAD = {
    "text": "Test 1",
    "url": "https://9gag.com/gag/amoNKdV",
    "tags": ["mosquito", "spray"],
    "info": {"colors": ["red", "white"], "objects": ["picture", "text"]},
}


def get_token_file_path():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    return os.path.join(current_directory, 'token.txt')


@pytest.fixture()
def token():
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


@pytest.fixture()
def meme_id(token):
    create_mem_pub = CreatePublication()
    payload = {
        "text": "Test 2",
        "url": "https://9gag.com/gag/amoNKdV",
        "tags": ["mosquito", "spray"],
        "info": {"colors": ["red", "white"], "objects": ["picture", "text"]},
    }
    create_mem_pub.create_new_publication(token=token, payload=payload)
    meme_id = create_mem_pub.response.json()['id']
    yield meme_id
    DeletePublication().delete_publication(token=token, meme_id=meme_id)


@pytest.fixture
def create_post():
    return CreatePublication()


@pytest.fixture
def get_id_post():
    return GetIdPublication()


@pytest.fixture
def put_post():
    return PutPublication()


@pytest.fixture
def delete_post():
    return DeletePublication()
