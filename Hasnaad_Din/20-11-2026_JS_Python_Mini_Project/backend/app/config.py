# config.py - reads secret settings from the .env file (never pushed to GitHub)
import os

from dotenv import load_dotenv

load_dotenv()  # copies the lines in .env into environment variables

DB_PASSWORD = os.getenv("DB_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
ALGORITHM = "HS256"
TOKEN_MINUTES = 60