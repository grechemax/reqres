"""Factory for generating test recipe data."""
import random
from typing import List, Dict, Any, Optional


class RecipeFactory:
    """Factory class for creating test recipe data."""

    CUISINES = ["Italian", "Chinese", "Mexican", "Japanese", "French", "Indian", "Thai", "American"]
    DIFFICULTIES = ["Easy", "Medium", "Hard"]
    MEAL_TYPES = ["Breakfast", "Lunch", "Dinner", "Snack", "Dessert"]

    SAMPLE_RECIPES = [
        {
            "name": "Creamy Mushroom Pasta",
            "cuisine": "Italian",
            "tags": ["Pasta", "Vegetarian", "Comfort Food"],
            "ingredients": [
                "Tagliatelle or fettuccine pasta",
                "Cremini mushrooms, sliced",
                "Garlic, minced",
                "Heavy cream",
                "Parmesan cheese, grated",
                "Fresh parsley, chopped",
                "Butter",
                "Olive oil",
                "Salt and black pepper",
                "Dry white wine (optional)"
            ],
            "instructions": [
                "Cook pasta in salted boiling water according to package instructions.",
                "In a large skillet, heat olive oil and butter over medium heat.",
                "Add sliced mushrooms and cook until golden brown.",
                "Add minced garlic and cook for 1 minute.",
                "Pour in white wine and let it reduce.",
                "Stir in heavy cream and simmer for 3-4 minutes.",
                "Add Parmesan and stir until sauce thickens.",
                "Toss pasta in sauce and season with salt and pepper.",
                "Garnish with fresh parsley before serving."
            ],
            "mealType": ["Dinner"],
            "servings": 4,
            "difficulty": "Easy",
            "prepTimeMinutes": 10,
            "cookTimeMinutes": 15,
            "caloriesPerServing": 520,
            "rating": 4.8
        },
        {
            "name": "Classic Margherita Pizza",
            "cuisine": "Italian",
            "tags": ["Pizza", "Vegetarian", "Classic"],
            "ingredients": [
                "Pizza dough",
                "Tomato sauce",
                "Fresh mozzarella",
                "Fresh basil leaves",
                "Olive oil",
                "Salt"
            ],
            "instructions": [
                "Preheat oven to 475°F (245°C).",
                "Roll out pizza dough on a floured surface.",
                "Spread tomato sauce evenly over dough.",
                "Add mozzarella slices.",
                "Drizzle with olive oil and sprinkle salt.",
                "Bake for 12-15 minutes until crust is golden.",
                "Top with fresh basil leaves before serving."
            ],
            "mealType": ["Lunch", "Dinner"],
            "servings": 2,
            "difficulty": "Medium",
            "prepTimeMinutes": 20,
            "cookTimeMinutes": 15,
            "caloriesPerServing": 680,
            "rating": 4.9
        },
        {
            "name": "Chicken Stir Fry",
            "cuisine": "Chinese",
            "tags": ["Chicken", "Quick", "Healthy"],
            "ingredients": [
                "Chicken breast, sliced",
                "Bell peppers",
                "Broccoli florets",
                "Soy sauce",
                "Garlic",
                "Ginger",
                "Sesame oil",
                "Cornstarch"
            ],
            "instructions": [
                "Marinate chicken in soy sauce and cornstarch.",
                "Heat oil in wok over high heat.",
                "Stir fry chicken until cooked through.",
                "Add vegetables and cook for 3-4 minutes.",
                "Add garlic and ginger.",
                "Drizzle with sesame oil and serve."
            ],
            "mealType": ["Lunch", "Dinner"],
            "servings": 4,
            "difficulty": "Easy",
            "prepTimeMinutes": 15,
            "cookTimeMinutes": 10,
            "caloriesPerServing": 320,
            "rating": 4.5
        }
    ]

    @staticmethod
    def create_recipe(
        name: Optional[str] = None,
        cuisine: Optional[str] = None,
        difficulty: Optional[str] = None,
        servings: Optional[int] = None,
        tags: Optional[List[str]] = None,
        ingredients: Optional[List[str]] = None,
        instructions: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a recipe with optional custom fields.

        Args:
            name: Recipe name
            cuisine: Cuisine type
            difficulty: Difficulty level (Easy, Medium, Hard)
            servings: Number of servings
            tags: List of tags
            ingredients: List of ingredients
            instructions: List of instruction steps
            **kwargs: Any additional fields to include

        Returns:
            Dictionary with recipe data wrapped in "data" key (reqres format)
        """
        # Use random sample as base if no name provided
        base_recipe = random.choice(RecipeFactory.SAMPLE_RECIPES).copy()

        recipe = {
            "name": name or base_recipe["name"],
            "cuisine": cuisine or base_recipe["cuisine"],
            "difficulty": difficulty or base_recipe["difficulty"],
            "servings": servings or base_recipe["servings"],
            "tags": tags or base_recipe["tags"],
            "ingredients": ingredients or base_recipe["ingredients"],
            "instructions": instructions or base_recipe["instructions"],
            "mealType": base_recipe.get("mealType", ["Dinner"]),
            "prepTimeMinutes": base_recipe.get("prepTimeMinutes", 15),
            "cookTimeMinutes": base_recipe.get("cookTimeMinutes", 20),
            "caloriesPerServing": base_recipe.get("caloriesPerServing", 400),
            "rating": base_recipe.get("rating", 4.5),
            "userId": random.randint(100, 999),
            "reviewCount": random.randint(10, 100),
            "image": f"https://cdn.dummyjson.com/recipe-images/{random.randint(1, 50)}.webp"
        }

        # Override with any additional kwargs
        recipe.update(kwargs)

        # Wrap in "data" key as required by reqres API
        return {"data": recipe}

    @staticmethod
    def create_simple_recipe(
        name: str = "Test Recipe",
        ingredients: Optional[List[str]] = None,
        instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a minimal recipe for simple testing.

        Args:
            name: Recipe name
            ingredients: List of ingredients (defaults to generic list)
            instructions: Instructions string (defaults to generic instructions)

        Returns:
            Dictionary with minimal recipe data wrapped in "data" key
        """
        return {
            "data": {
                "name": name,
                "ingredients": ingredients or ["ingredient 1", "ingredient 2", "ingredient 3"],
                "instructions": instructions or "Mix all ingredients and cook for 30 minutes",
                "cuisine": "Test Cuisine",
                "difficulty": "easy",
                "servings": 4
            }
        }

    @staticmethod
    def create_bulk_recipes(count: int = 5) -> List[Dict[str, Any]]:
        """
        Create multiple recipes for bulk testing.

        Args:
            count: Number of recipes to create

        Returns:
            List of recipe dictionaries
        """
        recipes = []
        for i in range(count):
            base = random.choice(RecipeFactory.SAMPLE_RECIPES)
            recipe = RecipeFactory.create_recipe(
                name=f"{base['name']} (Test {i+1})"
            )
            recipes.append(recipe)
        return recipes

    @staticmethod
    def create_recipe_with_missing_fields(**provided_fields) -> Dict[str, Any]:
        """
        Create a recipe with only specified fields (for negative testing).

        Args:
            **provided_fields: Only the fields you want to include

        Returns:
            Dictionary with only provided fields wrapped in "data" key
        """
        return {"data": provided_fields}

