"""Configuration and constants for the API."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

# Endpoint paths
RECIPES_PATH = "/collections/temp/records"

# Constructed endpoints
RECIPES_ENDPOINT = f"{BASE_URL}{RECIPES_PATH}"

