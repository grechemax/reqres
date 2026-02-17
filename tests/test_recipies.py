import requests
import pytest


def test_get_recipes_list(recipes_endpoint, api_headers):
    """GET /collections/recipes/records → should return 200 with recipes data."""
    response = requests.get(recipes_endpoint, headers=api_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (dict, list))


def test_get_recipes_with_valid_api_key(recipes_endpoint, api_headers):
    """Verify that valid API key returns successful response."""
    response = requests.get(recipes_endpoint, headers=api_headers)

    print(response.json())

    assert response.status_code == 200


def test_get_recipes_without_api_key(recipes_endpoint):
    """GET /collections/recipes/records without API key → should fail."""
    response = requests.get(recipes_endpoint)

    assert response.status_code >= 400
