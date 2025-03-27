import os
from dotenv import load_dotenv

load_dotenv(".env")

BOT_TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")
