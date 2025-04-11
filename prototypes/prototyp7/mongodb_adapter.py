import os
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


def read_chathistory(chat_id):
    response = ""
    data = col.find({'chat_id': chat_id}).sort('timestamp')
    for x in data:
        role = "User" if x['is_user'] else "Coach"
        response += f"{x['timestamp']} {role}: {x['message']} \n"
    return response

def read_chatids():
    return list(col.distinct("chat_id"))

chat_ids = read_chatids()
for chat_id in chat_ids:
    print(chat_id)