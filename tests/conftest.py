import os
import pytest
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")


# === FIXTURES ===

@pytest.fixture
def api_headers():
    """Fixture that provides valid API headers."""
    return {"x-api-key": API_KEY}


@pytest.fixture
def recipes_endpoint():
    """Fixture that provides the recipes endpoint URL."""
    return f"{BASE_URL}/collections/recipes/records"


@pytest.fixture
def api_client(api_headers):
    """Fixture that provides a preconfigured requests session."""
    session = requests.Session()
    session.headers.update(api_headers)
    return session

