import os

from dotenv import load_dotenv

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
HEROKU_URL = os.getenv('HEROKU_URL')
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")