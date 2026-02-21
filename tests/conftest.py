import pytest
import requests
from utils.recipe_factory import RecipeFactory
from utils.api_helper import RecipeAPIHelper
from utils.config import BASE_URL, API_KEY, RECIPES_ENDPOINT


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
