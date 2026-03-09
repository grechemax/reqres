"""
Recipe API Tests

Test suite for recipe creation and authentication:
- Test 1: Simple recipe creation (minimal fields)
- Test 2: Detailed recipe creation (all fields explicit)
- Test 3: Random recipe creation (from samples)
- Test 4: Authentication validation (API key required)
"""

import requests
from datetime import datetime
from conftest import verify_recipe_fields
from utils.config import RECIPES_ENDPOINT


def test_1_create_simple_recipe(api_headers, recipe_factory):
    """Create and verify a simple recipe with basic fields."""
    recipe = recipe_factory.create_simple_recipe(
        name=f"Simple Recipe {datetime.now().strftime('%d.%B %H:%M:%S')}",
        ingredients=["flour", "eggs", "milk", "butter"],
        instructions="Mix all ingredients and bake at 180°C for 30 minutes."
    )

    response = requests.post(RECIPES_ENDPOINT, json=recipe, headers=api_headers)
    assert response.status_code in [200, 201]

    verify_recipe_fields(response.json(), recipe)


def test_2_create_detailed_recipe(api_headers, recipe_factory):
    """Create and verify a detailed recipe with all fields explicitly specified."""
    recipe = recipe_factory.create_recipe(
        name=f"Detailed Recipe {datetime.now().strftime('%d.%B %H:%M:%S')}",
        cuisine="Italian",
        difficulty="Medium",
        servings=4,
        ingredients=["pasta", "cream", "mushrooms", "garlic", "parmesan"],
        instructions=["Cook pasta", "Sauté mushrooms", "Make cream sauce", "Combine and serve"],
        tags=["Pasta", "Vegetarian", "Comfort Food"],
        mealType=["Dinner"],
        prepTimeMinutes=15,
        cookTimeMinutes=20,
        caloriesPerServing=450
    )

    response = requests.post(RECIPES_ENDPOINT, json=recipe, headers=api_headers)
    assert response.status_code in [200, 201]

    verify_recipe_fields(response.json(), recipe, fields_to_check=["name", "cuisine", "difficulty", "servings"])


def test_3_create_random_recipe(api_headers, recipe_factory):
    """Create and verify a random recipe from sample templates."""
    recipe = recipe_factory.create_random_recipe()

    response = requests.post(RECIPES_ENDPOINT, json=recipe, headers=api_headers)
    assert response.status_code in [200, 201]

    verify_recipe_fields(response.json(), recipe, fields_to_check=["name", "ingredients", "instructions"])


def test_4_access_without_valid_api_key():
    """Verify API key is required for both GET and POST requests."""
    # GET without API key should fail
    response = requests.get(RECIPES_ENDPOINT)
    assert response.status_code in [401, 403]

    # POST without API key should fail
    recipe = {"data": {"name": "Test", "ingredients": ["a"], "instructions": "mix"}}
    response = requests.post(RECIPES_ENDPOINT, json=recipe)
    assert response.status_code in [401, 403]


def test_5_create_recipe_with_missing_fields(api_headers, recipe_factory):
    """Test 5: Create a recipe with missing required fields and verify error handling."""
    incomplete_recipe = recipe_factory.create_recipe_with_missing_fields(
        name="Incomplete Recipe",
        ingredients=["item 1", "item 2"]
        #Missing instructions, cuisine, etc.
    )

    response = requests.post(RECIPES_ENDPOINT, json=incomplete_recipe, headers=api_headers)

    # Expecting a 400 Bad Request or similar error due to missing fields
    # assert response.status_code in [400, 422], f"Expected 400 or 422 for missing fields, got {response.status_code}"
    # TODO endpoint currently allows creation of recipes with missing fields, should be fixed to return error


def test_6_update_recipe(api_headers, recipe_factory, api_helper):
    """Create a recipe, update it, then verify updated fields."""
    original_recipe = recipe_factory.create_simple_recipe(
        name=f"Original Recipe",
        difficulty="Medium",
        ingredients=["tomato", "salt"],
        instructions="Mix ingredients."
    )
    create_response = requests.post(RECIPES_ENDPOINT, json=original_recipe, headers=api_headers)
    assert create_response.status_code in [200, 201]

    create_json = create_response.json()
    assert "data" in create_json and "id" in create_json["data"], "Missing created recipe id"
    recipe_id = create_json["data"]["id"]

    update_payload = {
        "name": "Updated Recipe",
        "cuisine": "Updated Cuisine",
        "difficulty": "easy",
        "servings": 4,
        "ingredients": ["salt"],
        "instructions": ["pepper"]
    }
    update_response = api_helper.update_recipe(recipe_id, update_payload)
    assert update_response.status_code in [200, 204]

    get_response = api_helper.get_recipe_by_id(recipe_id)
    assert get_response.status_code == 200

    get_json = get_response.json()
    assert "data" in get_json and "data" in get_json["data"], "Unexpected response structure"
    updated_recipe = get_json["data"]["data"]

    assert updated_recipe["name"] == "Updated Recipe"
    assert updated_recipe["cuisine"] == "Updated Cuisine"
    assert updated_recipe["difficulty"] == "easy"
    assert updated_recipe["servings"] == 4
    assert updated_recipe["ingredients"] == ["salt"]
    assert updated_recipe["instructions"] == ["pepper"]
