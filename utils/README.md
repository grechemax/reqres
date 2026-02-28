# Utils Package

This package contains utilities for API testing, including configuration, data factories, and API helpers.

## Structure

```
utils/
├── __init__.py              # Package initialization
├── config.py                # Centralized configuration (API URLs, keys, paths)
├── recipe_factory.py        # Factory for generating test recipe data (no defaults philosophy)
├── recipe_samples.py        # Sample recipes for factory templates (8 cuisines, 3 difficulties)
├── api_helper.py            # Helper class for API operations
├── recipe_schema.json       # Recipe data schema
└── README.md                # This file
```


## Usage

### 1. RecipeFactory (for test data)

**Philosophy**: All parameters are explicit - no hidden defaults. Tests fully control their data.

```python
from utils.recipe_factory import RecipeFactory

# Simple recipe (minimal fields, sensible test defaults for cuisine/difficulty/servings)
recipe = RecipeFactory.create_simple_recipe(
    name="Pancakes",
    ingredients=["flour", "eggs", "milk"],
    instructions="Mix and cook on griddle"
)

# Detailed recipe (ALL parameters required - explicit and visible)
recipe = RecipeFactory.create_recipe(
    name="Spaghetti Carbonara",
    cuisine="Italian",
    difficulty="Medium",
    servings=2,
    ingredients=["pasta", "eggs", "guanciale", "pecorino"],
    instructions=["Boil pasta", "Cook guanciale", "Mix eggs", "Combine"],
    tags=["Pasta", "Italian", "Classic"],
    mealType=["Dinner"],
    prepTimeMinutes=10,
    cookTimeMinutes=20,
    caloriesPerServing=380
)

# Random recipe from templates (quick testing, no parameters needed)
recipe = RecipeFactory.create_random_recipe()

# Bulk recipes for load testing
recipes = RecipeFactory.create_bulk_recipes(count=10)

# Negative testing - only specified fields
incomplete_recipe = RecipeFactory.create_recipe_with_missing_fields(
    name="Incomplete",
    ingredients=["flour"]
    # Missing 'instructions' - useful for API validation tests
)
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

# Cleanup multiple recipes by IDs
api.cleanup_test_recipes(["id1", "id2", "id3"])

# Delete ALL recipes (useful for test teardown)
api.delete_all_recipes()
```

### 3. In Pytest Tests

Using the `verify_recipe_fields` helper to validate created recipes:

```python
from conftest import verify_recipe_fields

def test_create_recipe(recipe_factory, api_helper):
    """Using factory and helper fixtures."""
    # Generate test data
    recipe = recipe_factory.create_detailed_recipe(
        name="Test Pizza",
        cuisine="Italian",
        difficulty="Easy",
        servings=2,
        ingredients=["dough", "sauce", "cheese"],
        instructions=["Mix", "Bake"],
        tags=["Pizza"],
        mealType=["Dinner"],
        prepTimeMinutes=10,
        cookTimeMinutes=15,
        caloriesPerServing=300
    )
    
    # Use helper to interact with API
    response = api_helper.create_recipe(recipe)
    
    # Verify response
    assert response.status_code in [200, 201]
    
    # Verify all fields match (or specific fields)
    verify_recipe_fields(response.json(), recipe)
    
    # Or check only specific fields
    verify_recipe_fields(response.json(), recipe, fields_to_check=["name", "cuisine"])
```

Or using granular fixtures with requests:

```python
import requests

def test_create_recipe(recipes_endpoint, api_headers, recipe_factory):
    """Using granular fixtures."""
    recipe = recipe_factory.create_simple_recipe(
        name="Test Pizza",
        ingredients=["dough", "sauce", "cheese"],
        instructions="Mix and bake"
    )
    
    response = requests.post(recipes_endpoint, json=recipe, headers=api_headers)
    
    assert response.status_code in [200, 201]
    
    verify_recipe_fields(response.json(), recipe)
```

**Note**: The `cleanup_recipes_after_test` fixture automatically runs after each test to keep the system clean.

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

## Test Fixtures & Automatic Cleanup

All fixtures are defined in `conftest.py`:

- **`api_headers`**: API headers with authentication key
- **`recipes_endpoint`**: Full recipes endpoint URL
- **`api_client`**: Pre-configured requests session
- **`recipe_factory`**: RecipeFactory instance for test data
- **`api_helper`**: RecipeAPIHelper instance for API operations
- **`cleanup_recipes_after_test`** (autouse): Automatically deletes all recipes after each test completes

The automatic cleanup fixture ensures:
- Each test starts with a clean state
- No data pollution between tests
- Recipes created during tests don't accumulate
- Tests remain isolated and repeatable

To disable cleanup for a specific test, simply don't use the fixture (fixtures can be individually disabled in pytest).

## Test Structure

Recipe API tests (`tests/test_recipies.py`):

1. **test_1_create_simple_recipe** - Create and verify a simple recipe (minimal fields)
2. **test_2_create_detailed_recipe** - Create and verify a detailed recipe (all fields explicit)
3. **test_3_create_random_recipe** - Create and verify a random recipe (from samples)
4. **test_4_access_without_valid_api_key** - Verify authentication is required (both GET and POST)

