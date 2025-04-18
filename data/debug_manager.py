# SETUP
import os

import pymongo
from dotenv import load_dotenv

load_dotenv()
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client["proactive-behaviour"]
col_debug = db["debug"]

result = col_debug.delete_many({})
