import pytest
import requests
from typing import Dict, Any, List
from utils.recipe_factory import RecipeFactory
from utils.api_helper import RecipeAPIHelper
from utils.config import BASE_URL, API_KEY, RECIPES_ENDPOINT


# === HELPER FUNCTIONS ===

def verify_recipe_fields(response_json: Dict[str, Any], expected_recipe: Dict[str, Any], fields_to_check: List[str] = None):
    """
    Helper function to verify that created recipe matches expected recipe.

    Args:
        response_json: The response JSON from API containing the created recipe
        expected_recipe: The original recipe data that was sent
        fields_to_check: List of fields to verify. If None, checks all common fields.
    """
    assert "data" in response_json, "Response should have 'data' key"

    created_recipe_data = response_json["data"]
    created_recipe = created_recipe_data["data"]
    expected_data = expected_recipe["data"]

    print("Created Recipe:", created_recipe)

    # Default fields to check if not specified
    if fields_to_check is None:
        fields_to_check = ["name", "ingredients", "instructions", "cuisine", "difficulty", "servings"]

    for field in fields_to_check:
        if field in expected_data:
            assert created_recipe[field] == expected_data[field], f"Field '{field}' mismatch"

    return created_recipe


# === FIXTURES ===

@pytest.fixture
def api_headers():
    """Fixture that provides valid API headers."""
    return {"x-api-key": API_KEY}


@pytest.fixture
def recipes_endpoint():
    """Fixture that provides the recipes endpoint URL."""
    return RECIPES_ENDPOINT


@pytest.fixture
def api_client(api_headers):
    """Fixture that provides a preconfigured requests session."""
    session = requests.Session()
    session.headers.update(api_headers)
    return session


@pytest.fixture
def recipe_factory():
    """Fixture that provides the RecipeFactory for generating test data."""
    return RecipeFactory


@pytest.fixture
def api_helper():
    """Fixture that provides a RecipeAPIHelper instance."""
    return RecipeAPIHelper(BASE_URL, API_KEY)


# @pytest.fixture(autouse=True)
# def cleanup_recipes_after_test(api_helper):
#     """Automatically delete all recipes after each test."""
#     yield
#     # Cleanup after test completes
#     api_helper.delete_all_recipes()

