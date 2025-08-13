from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
MONGO_URL = getenv("MONGO_URL")

if not all([API_ID, API_HASH, BOT_TOKEN, MONGO_URL]):
    raise ValueError("Missing one or more essential environment variables.")
