import os

import pymongo
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client["proactive-behaviour"]
col = db["test"]

query_filter = { "chat_id": TELEGRAM_CHAT_ID}
result = col.delete_many(query_filter)
