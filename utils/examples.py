"""
Examples of using RecipeFactory for dynamic test data generation.

This module demonstrates various ways to use the RecipeFactory to generate
test recipe data dynamically in your tests.
"""

from utils.recipe_factory import RecipeFactory


# Example 1: Create a simple recipe with minimal fields
def example_simple_recipe():
    """Create a simple recipe for basic testing."""
    recipe = RecipeFactory.create_simple_recipe(
        name="Simple Pancakes",
        ingredients=["flour", "eggs", "milk", "butter"],
        instructions="Mix all ingredients and cook on griddle"
    )
    print("Simple Recipe:", recipe)
    return recipe


# Example 2: Create a detailed recipe with custom fields
def example_detailed_recipe():
    """Create a detailed recipe with specific attributes."""
    recipe = RecipeFactory.create_recipe(
        name="Spaghetti Carbonara",
        cuisine="Italian",
        difficulty="Medium",
        servings=2,
        tags=["Pasta", "Italian", "Quick"],
        ingredients=[
            "Spaghetti pasta",
            "Eggs",
            "Parmesan cheese",
            "Pancetta",
            "Black pepper"
        ],
        instructions=[
            "Cook pasta according to package directions",
            "Fry pancetta until crispy",
            "Mix eggs and parmesan",
            "Combine everything and serve"
        ]
    )
    print("Detailed Recipe:", recipe)
    return recipe


# Example 3: Create a random recipe from templates
def example_random_recipe():
    """Generate a random recipe from predefined templates."""
    recipe = RecipeFactory.create_recipe()
    print("Random Recipe:", recipe)
    return recipe


# Example 4: Create multiple recipes for bulk testing
def example_bulk_recipes():
    """Create multiple recipes at once."""
    recipes = RecipeFactory.create_bulk_recipes(count=5)
    print(f"Created {len(recipes)} recipes")
    for i, recipe in enumerate(recipes, 1):
        print(f"{i}. {recipe['data']['name']}")
    return recipes


# Example 5: Create recipe with missing fields (negative testing)
def example_incomplete_recipe():
    """Create a recipe with only some fields for negative testing."""
    recipe = RecipeFactory.create_recipe_with_missing_fields(
        name="Incomplete Recipe",
        ingredients=["item 1", "item 2"]
        # Note: missing required fields like instructions, cuisine, etc.
    )
    print("Incomplete Recipe:", recipe)
    return recipe


# Example 6: Use in a pytest test
def example_pytest_usage():
    """
    Example test using RecipeFactory (pseudo-code).

    def test_create_recipe(recipes_endpoint, api_headers, recipe_factory):
        # Create a test recipe
        new_recipe = recipe_factory.create_recipe(
            name="Test Tacos",
            cuisine="Mexican",
            difficulty="Easy"
        )

        # Post to API
        response = requests.post(recipes_endpoint, json=new_recipe, headers=api_headers)

        # Assertions
        assert response.status_code in [200, 201]
        assert response.json()["data"]["name"] == "Test Tacos"
    """
    pass


# Example 7: Customize with additional fields
def example_custom_fields():
    """Add custom fields beyond the standard ones."""
    recipe = RecipeFactory.create_recipe(
        name="Vegan Buddha Bowl",
        cuisine="Asian Fusion",
        difficulty="Easy",
        isVegan=True,
        isDairyFree=True,
        nutritionInfo={
            "protein": "15g",
            "carbs": "45g",
            "fat": "12g"
        }
    )
    print("Custom Fields Recipe:", recipe)
    return recipe


if __name__ == "__main__":
    print("=" * 60)
    print("RecipeFactory Usage Examples")
    print("=" * 60)

    print("\n1. Simple Recipe:")
    example_simple_recipe()

    print("\n2. Detailed Recipe:")
    example_detailed_recipe()

    print("\n3. Random Recipe:")
    example_random_recipe()

    print("\n4. Bulk Recipes:")
    example_bulk_recipes()

    print("\n5. Incomplete Recipe (for negative testing):")
    example_incomplete_recipe()

    print("\n6. Custom Fields Recipe:")
    example_custom_fields()

    print("\n" + "=" * 60)
    print("See test_recipies.py for real test examples!")
    print("=" * 60)

