from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
MONGO_URL = getenv("MONGO_URL")
GEMINI_API_KEY = getenv("GEMINI_API_KEY")

if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URL, GEMINI_API_KEY]):
    raise ValueError("Missing one or more essential environment variables.")
