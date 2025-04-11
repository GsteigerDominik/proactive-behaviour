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


def insert_message(szenario,datetime, is_user, message):
    #Define bevor usage
    col.insert_one(
        {
            "chat_id": szenario,
            "timestamp": datetime,
            "is_user": is_user,
            "message": message

        }
    )

#Szenario 1 Getting Back into Running
#Scenario 2: “The Motivated Student” (Goal: Daily Study Habit)
#Scenario 3: “The Ghosting User” (Goal: Meditate 3x/week)
szenario = [
    # Day 1 – Goal Setting (2025-04-08)
    {'datetime': '2025-04-11 14:00:00',
     'is_user': False,
     'message': 'Hallo, Ich bin dein Coach und hier, um dich bei deinen Zielen zu unterstützen. Sag mir einfach, wer du bist und was du erreichen möchtest!'},
]

for chat in szenario:
    insert_message('Anna Albrecht',
        datetime.strptime(chat['datetime'], '%Y-%m-%d %H:%M:%S'),chat['is_user'],chat['message'])