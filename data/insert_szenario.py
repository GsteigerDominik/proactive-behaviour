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
            "chat_id": 'Szenario-03',
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
    {'datetime': '2025-04-08 14:00:00', 'is_user': True, 'message': 'I’d like to start meditating more regularly. I feel stressed lately.'},
    {'datetime': '2025-04-08 14:01:00', 'is_user': False, 'message': 'Good call – meditation can really help. Want to aim for 3 sessions this week, 10 minutes each?'},
    {'datetime': '2025-04-08 14:01:45', 'is_user': True, 'message': 'Sounds good. Let’s do it.'},
    {'datetime': '2025-04-08 14:03:00', 'is_user': False, 'message': 'Great! Want me to remind you in the evenings or mornings?'},
    {'datetime': '2025-04-08 14:04:00', 'is_user': True, 'message': 'Evenings would be better.'},
    {'datetime': '2025-04-08 14:05:00', 'is_user': False, 'message': 'Got it. Let’s try for your first session tonight after 8 PM.'},

    # Day 2 (2025-04-09) – No Response
    {'datetime': '2025-04-09 20:00:00', 'is_user': False, 'message': 'Hey, how are you feeling tonight? Ready for a short meditation session?'},

    # Day 3 (2025-04-10) – Still No Response
    {'datetime': '2025-04-10 20:15:00', 'is_user': False, 'message': 'Just checking in. Haven’t heard from you – everything okay? Remember, it’s okay to restart anytime.'}
]

for chat in szenario:
    insert_message(datetime.strptime(chat['datetime'], '%Y-%m-%d %H:%M:%S'),chat['is_user'],chat['message'])