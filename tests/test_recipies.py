import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

def test_get_recipes_list():
    headers = {"x-api-key": API_KEY}
    response = requests.get(f"{BASE_URL}/collections/recipes/records", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (dict, list))


def test_get_recipes_with_valid_api_key():
    headers = {"x-api-key": API_KEY}
    response = requests.get(f"{BASE_URL}/collections/recipes/records", headers=headers)

    assert response.status_code == 200


def test_get_recipes_without_api_key():
    response = requests.get(f"{BASE_URL}/collections/recipes/records")

    assert response.status_code != 200
