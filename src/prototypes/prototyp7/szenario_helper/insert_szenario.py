import os
from datetime import datetime, timedelta

import pymongo
from dotenv import load_dotenv

# SETUP
load_dotenv()
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client["proactive-behaviour"]
col = db["test"]


def insert_message(datetime, is_user, message):
    #Define bevor usage
    col.insert_one(
        {
            "chat_id": TELEGRAM_CHAT_ID,
            "timestamp": datetime,
            "is_user": is_user,
            "message": message

        }
    )


yesterday = datetime.now() - timedelta(days=1)

insert_message(yesterday.replace(hour=8, minute=0, second=0),
               True,
               "I want to practice guitar for 30 minutes every other day.")

insert_message(yesterday.replace(hour=8, minute=5, second=0),
               False,
               "Nice goal!, so i will here from you tommorow!")
