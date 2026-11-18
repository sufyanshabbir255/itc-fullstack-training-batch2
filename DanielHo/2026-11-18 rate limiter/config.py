import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    RATE_LIMIT = os.getenv(
        "RATE_LIMIT",       # This looks for .env setting
        "5/minute"          # If not found, defaults to this
    )

print(Settings.RATE_LIMIT)