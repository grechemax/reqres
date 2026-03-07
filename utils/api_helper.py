"""Helper functions for API operations with recipes."""
import requests
from typing import Dict, Any, List
from .config import RECIPES_ENDPOINT


class RecipeAPIHelper:
    """Helper class for common API operations with recipes."""

    def __init__(self, api_key: str):
        """
        Initialize the helper with API credentials.

        Args:
            api_key: API key for authentication
        """
        self.headers = {"x-api-key": api_key}
        self.recipes_endpoint = RECIPES_ENDPOINT

    def create_recipe(self, recipe_data: Dict[str, Any]) -> requests.Response:
        return requests.post(self.recipes_endpoint, json=recipe_data, headers=self.headers)

    def get_all_recipes(self) -> requests.Response:
        return requests.get(self.recipes_endpoint, headers=self.headers)

    def get_recipe_by_id(self, recipe_id: str) -> requests.Response:
        url = f"{self.recipes_endpoint}/{recipe_id}"
        return requests.get(url, headers=self.headers)

    def update_recipe(self, recipe_id: str, recipe_data: Dict[str, Any]) -> requests.Response:
        url = f"{self.recipes_endpoint}/{recipe_id}"
        return requests.patch(url, json=recipe_data, headers=self.headers)

    def delete_recipe(self, recipe_id: str) -> requests.Response:
        url = f"{self.recipes_endpoint}/{recipe_id}"
        return requests.delete(url, headers=self.headers)

    def delete_all_recipes(self) -> None:
        """Delete all recipes from the collection."""
        response = self.get_all_recipes()
        if response.status_code == 200:
            response_json = response.json()
            if "data" in response_json:
                recipes = response_json["data"]
                for record in recipes:
                    # Extract recipe ID from the record
                    if "id" in record:
                        self.delete_recipe(record["id"])
