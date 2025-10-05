# API Configuration for Monthly Pack Agent
# All APIs used are FREE

import os
from pathlib import Path

def load_env_file():
    """Load environment variables from api_keys.env file"""
    env_file = Path(__file__).parent / "api_keys.env"
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# Load environment variables
load_env_file()

# TMDB (The Movie Database) - FREE
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "test_key")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Google Books API - FREE
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY", "test_key")
GOOGLE_BOOKS_BASE_URL = "https://www.googleapis.com/books/v1"

# iTunes Podcasts - FREE (no key needed)
ITUNES_BASE_URL = "https://itunes.apple.com/search"

# Email settings (optional)
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "False").lower() == "true"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "swapna@example.com")