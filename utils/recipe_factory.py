"""Factory for generating test recipe data."""
import random
from typing import List, Dict, Any

from utils.recipe_samples import SAMPLE_RECIPES


class RecipeFactory:
    """
    Factory class for creating test recipe data with explicit, no-default parameters.

    All parameters must be explicitly provided by tests to ensure clarity and control
    over test data. No hidden defaults are applied by the factory.
    """

    @staticmethod
    def _wrap_recipe(recipe_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wrap recipe data in the reqres API format.

        Args:
            recipe_data: The recipe dictionary to wrap

        Returns:
            Recipe wrapped in "data" key as required by reqres API
        """
        return {"data": recipe_data}

    @staticmethod
    def create_recipe(
        name: str,
        cuisine: str,
        difficulty: str,
        servings: int,
        ingredients: List[str],
        instructions: List[str],
        tags: List[str],
        mealType: List[str],
        prepTimeMinutes: int,
        cookTimeMinutes: int,
        caloriesPerServing: int
    ) -> Dict[str, Any]:
        """
        Create a detailed recipe with all explicit parameters.

        This method requires all parameters to be explicitly provided - no defaults.
        Use this for creating recipes with specific test values.

        Args:
            name: Recipe name (e.g., "Spaghetti Carbonara")
            cuisine: Cuisine type (e.g., "Italian", "Thai")
            difficulty: Difficulty level (e.g., "Easy", "Medium", "Hard")
            servings: Number of servings (e.g., 4)
            ingredients: List of ingredient strings (e.g., ["pasta", "eggs", "bacon"])
            instructions: List of instruction steps (e.g., ["Boil water", "Cook pasta"])
            tags: List of recipe tags (e.g., ["Pasta", "Quick", "Vegetarian"])
            mealType: List of meal types (e.g., ["Dinner", "Lunch"])
            prepTimeMinutes: Preparation time in minutes (e.g., 10)
            cookTimeMinutes: Cooking time in minutes (e.g., 20)
            caloriesPerServing: Calories per serving (e.g., 450)

        Returns:
            Dictionary with recipe data wrapped in "data" key (reqres format)
        """
        recipe = {
            "name": name,
            "cuisine": cuisine,
            "difficulty": difficulty,
            "servings": servings,
            "ingredients": ingredients,
            "instructions": instructions,
            "tags": tags,
            "mealType": mealType,
            "prepTimeMinutes": prepTimeMinutes,
            "cookTimeMinutes": cookTimeMinutes,
            "caloriesPerServing": caloriesPerServing,
        }
        return RecipeFactory._wrap_recipe(recipe)

    @staticmethod
    def create_random_recipe() -> Dict[str, Any]:
        """
        Create a random recipe from predefined sample templates.

        This method selects a random recipe from SAMPLE_RECIPES with all fields
        already populated. Use this for quick random testing without specifying
        individual parameters.

        Returns:
            Dictionary with random recipe data wrapped in "data" key
        """
        base_recipe = random.choice(SAMPLE_RECIPES).copy()
        return RecipeFactory._wrap_recipe(base_recipe)

    @staticmethod
    def create_simple_recipe(
        name: str,
        ingredients: List[str],
        instructions: str,
        cuisine: str = "Test Cuisine",
        difficulty: str = "easy",
        servings: int = 4
    ) -> Dict[str, Any]:
        """
        Create a minimal recipe with only essential fields.

        This method is for simple unit tests that focus on name, ingredients,
        and instructions. Other fields have sensible test defaults.

        Args:
            name: Recipe name (required)
            ingredients: List of ingredients (required)
            instructions: Instructions as a single string (required)
            cuisine: Cuisine type (default: "Test Cuisine")
            difficulty: Difficulty level (default: "easy")
            servings: Number of servings (default: 4)

        Returns:
            Dictionary with minimal recipe data wrapped in "data" key
        """
        recipe = {
            "name": name,
            "ingredients": ingredients,
            "instructions": instructions,
            "cuisine": cuisine,
            "difficulty": difficulty,
            "servings": servings
        }
        return RecipeFactory._wrap_recipe(recipe)

    @staticmethod
    def create_bulk_recipes(count: int = 5) -> List[Dict[str, Any]]:
        """
        Create multiple random recipes for bulk testing.

        Each recipe is assigned a unique name by appending "(Test N)" to make
        them distinguishable in tests.

        Args:
            count: Number of recipes to create (default: 5)

        Returns:
            List of recipe dictionaries, each with unique names
        """
        recipes = []
        for i in range(count):
            recipe = RecipeFactory.create_random_recipe()
            # Make name unique for bulk testing
            recipe["data"]["name"] = f"{recipe['data']['name']} (Test {i+1})"
            recipes.append(recipe)
        return recipes

    @staticmethod
    def create_recipe_with_missing_fields(**provided_fields) -> Dict[str, Any]:
        """
        Create a recipe with only specified fields (for negative testing).

        This is useful for testing API validation - you can omit required fields
        to verify the API properly rejects invalid recipes.

        Args:
            **provided_fields: Only the fields you want to include in the recipe

        Returns:
            Dictionary with only provided fields wrapped in "data" key

        Example:
            # Create recipe missing the 'ingredients' field
            recipe = RecipeFactory.create_recipe_with_missing_fields(
                name="Incomplete Recipe",
                instructions=["Step 1"]
            )
        """
        return RecipeFactory._wrap_recipe(provided_fields)
