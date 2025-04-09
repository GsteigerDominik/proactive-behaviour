import os
from datetime import datetime

import pymongo
from dotenv import load_dotenv

# SETUP
load_dotenv()
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client["proactive-behaviour"]
col = db["test"]


def insert_message(chat_id, datetime, is_user, message):
    col.insert_one(
        {
            "chat_id": chat_id,
            "timestamp": datetime,
            "is_user": is_user,
            "message": message

        }
    )


insert_message("szenario_a",
               datetime(2025, 4, 4, 8, 0, 0),
               True,
               "I want to practice guitar for 30 minutes every other day.")

insert_message("szenario_a",
               datetime(2025, 4, 4, 8, 5, 0),
               False,
               "Nice goal!")

insert_message("szenario_a",
               datetime(2025, 4, 4, 11, 30, 0),
               True,
               "I am really struggling to get motivated, do you got any Tipps?")