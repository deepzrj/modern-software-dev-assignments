import os
from dotenv import load_dotenv
from pathlib import Path

# Get project root (base-repo)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env explicitly
load_dotenv(BASE_DIR / ".env")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"