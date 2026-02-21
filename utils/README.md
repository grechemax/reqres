# Utils Package

This package contains utilities for API testing, including configuration, data factories, and API helpers.

## Structure

```
utils/
├── __init__.py          # Package initialization
├── config.py            # Centralized configuration (API URLs, keys, paths)
├── recipe_factory.py    # Factory for generating test recipe data
├── api_helper.py        # Helper class for API operations
└── examples.py          # Usage examples
```


## Usage

### 1. RecipeFactory (for test data)

```python
from utils.recipe_factory import RecipeFactory

# Simple recipe
recipe = RecipeFactory.create_simple_recipe(
    name="Pancakes",
    ingredients=["flour", "eggs", "milk"]
)

# Detailed recipe
recipe = RecipeFactory.create_recipe(
    name="Spaghetti Carbonara",
    cuisine="Italian",
    difficulty="Medium",
    servings=2
)

# Random recipe from templates
recipe = RecipeFactory.create_recipe()

# Bulk recipes
recipes = RecipeFactory.create_bulk_recipes(count=10)
```

### 2. RecipeAPIHelper (for API operations)

```python
from utils.api_helper import RecipeAPIHelper
from utils.config import BASE_URL, API_KEY

# Initialize helper
api = RecipeAPIHelper(BASE_URL, API_KEY)

# Create recipe
response = api.create_recipe(recipe_data)

# Get all recipes
response = api.get_all_recipes()

# Get by ID
response = api.get_recipe_by_id("123")

# Update recipe
response = api.update_recipe("123", updated_data)

# Delete recipe
response = api.delete_recipe("123")

# Cleanup multiple recipes
api.cleanup_test_recipes(["id1", "id2", "id3"])
```

### 3. In Pytest Tests

```python
def test_create_recipe(recipe_factory, api_helper):
    """Using both factory and helper fixtures."""
    # Generate test data
    new_recipe = recipe_factory.create_recipe(name="Test Pizza")
    
    # Use helper to interact with API
    response = api_helper.create_recipe(new_recipe)
    
    assert response.status_code in [200, 201]
```

Or using individual fixtures:

```python
def test_create_recipe(recipes_endpoint, api_headers, recipe_factory):
    """Using granular fixtures."""
    new_recipe = recipe_factory.create_recipe(name="Test Pizza")
    response = requests.post(recipes_endpoint, json=new_recipe, headers=api_headers)
    assert response.status_code in [200, 201]
```

## Configuration Management

All API endpoints, keys, and paths are managed in `config.py`:

- **BASE_URL**: Loaded from `.env` file
- **API_KEY**: Loaded from `.env` file  
- **RECIPES_PATH**: Defined once, used everywhere
- **RECIPES_ENDPOINT**: Pre-constructed full endpoint URL

This ensures consistency across:
- Test fixtures (conftest.py)
- API helpers (api_helper.py)
- Any other modules that need to interact with the API

## Adding New Endpoints

To add a new endpoint path:

1. Add the path constant to `config.py`:
   ```python
   USERS_PATH = "/api/users"
   USERS_ENDPOINT = f"{BASE_URL}{USERS_PATH}"
   ```

2. Use it in your fixtures or helpers:
   ```python
   from utils.config import USERS_ENDPOINT
   ```

3. Done! No duplication needed.

