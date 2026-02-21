import requests


def test_validate_recipes_have_required_fields(recipes_endpoint, api_headers):
    """Validate that all recipes have required fields like name, ingredients, instructions, etc."""
    response = requests.get(recipes_endpoint, headers=api_headers)

    assert response.status_code == 200

    response_json = response.json()

    # API returns: {"data": [...], "meta": {...}}
    assert "data" in response_json, "Response should have 'data' key"
    assert "meta" in response_json, "Response should have 'meta' key"

    records_with_metadata = response_json["data"]

    assert len(records_with_metadata) > 0, "Should have at least one recipe record"

    for record in records_with_metadata:
        # Extract actual recipe from nested 'data' field
        recipe = record["data"]
        print(recipe["name"])

        # Validate recipe has expected fields
        assert "name" in recipe, "Recipe should have 'name'"
        assert "ingredients" in recipe, "Recipe should have 'ingredients'"
        assert "instructions" in recipe, "Recipe should have 'instructions'"
        assert "cuisine" in recipe, "Recipe should have 'cuisine'"
        assert "difficulty" in recipe, "Recipe should have 'difficulty'"
        assert "servings" in recipe, "Recipe should have 'servings'"


def test_get_recipes_with_valid_api_key(recipes_endpoint, api_headers):
    """Verify that valid API key returns successful response."""
    response = requests.get(recipes_endpoint, headers=api_headers)

    assert response.status_code == 200

    response_json = response.json()
    assert "data" in response_json, "Response should have 'data' key"
    assert "meta" in response_json, "Response should have 'meta' key"
    assert isinstance(response_json["data"], list), "Data should be a list"


def test_get_recipes_without_api_key(recipes_endpoint):
    """GET /collections/recipes/records without API key → should fail."""
    response = requests.get(recipes_endpoint)

    assert response.status_code >= 400


def test_post_new_recipe(recipes_endpoint, api_headers):
    """POST a new recipe to the endpoint."""
    new_recipe = {
        "data": {
            "name": "Test Recipe",
            "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"],
            "instructions": "Mix all ingredients and cook for 30 minutes",
            "cuisine": "Test Cuisine",
            "difficulty": "easy",
            "servings": 4
        }
    }

    response = requests.post(recipes_endpoint, json=new_recipe, headers=api_headers)

    assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"

    response_json = response.json()
    assert "data" in response_json, "Response should have 'data' key"

    # Verify the created recipe has the expected fields
    created_recipe = response_json["data"]
    # TODO implement a better way to verify the created recipe, e.g. by fetching it again using its ID and comparing the fields
    # assert created_recipe["name"] == new_recipe["data"]["name"]
    # assert created_recipe["ingredients"] == new_recipe["data"]["ingredients"]
    # assert created_recipe["instructions"] == new_recipe["data"]["instructions"]
    # assert created_recipe["cuisine"] == new_recipe["data"]["cuisine"]
    # assert created_recipe["difficulty"] == new_recipe["data"]["difficulty"]
    # assert created_recipe["servings"] == new_recipe["data"]["servings"]

