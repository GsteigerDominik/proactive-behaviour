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
            "chat_id": 'test_auto_11-04',
            "timestamp": datetime,
            "is_user": is_user,
            "message": message

        }
    )

szenario = [
    {'datetime':'2025-04-11 08:00:00',
     'is_user':True,
     'message':'Hallo'
     },
    {'datetime':'2025-04-11 08:05:00',
     'is_user':False,
     'message':'Hey wie geht es dir?'
     }
]

for chat in szenario:
    insert_message(datetime.strptime(chat['datetime'], '%Y-%m-%d %H:%M:%S'),chat['is_user'],chat['message'])