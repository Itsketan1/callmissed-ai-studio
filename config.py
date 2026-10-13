
import os
from dotenv import load_dotenv

load_dotenv(".env")

API_KEY = os.getenv("CALLMISSED_API_KEY", "").strip()
API_BASE_URL = "https://api.callmissed.com/v1"
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"


def validate_config():
    if not API_KEY:
        raise RuntimeError(
            "CALLMISSED_API_KEY is missing. Check your .env file."
        )
