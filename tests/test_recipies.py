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
