import os

import pymongo
from dotenv import load_dotenv

# SETUP
load_dotenv()
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client["proactive-behaviour"]
col = db["test"]
col_debug = db["debug"]


def insert_message(chat_id, datetime, is_user, message):
    col.insert_one(
        {
            "chat_id": chat_id,
            "timestamp": datetime,
            "is_user": is_user,
            "message": message

        }
    )


def insert_debug(datetime,prompt):
    col_debug.insert_one({
        "timestamp": datetime,
        "prompt": prompt
    })

def read_chathistory_string(chat_id):
    response = ""
    data = col.find({'chat_id': chat_id}).sort('timestamp')
    for x in data:
        role = "User" if x['is_user'] else "Coach"
        response += f"{x['timestamp']} {role}: {x['message']} \n"
    return response


def read_chathistory_json(chat_id):
    data = list(col.find({'chat_id': chat_id}).sort('timestamp'))
    for x in data:
        x['_id'] = str(x['_id'])
    return data


def read_chatoverview():
    pipeline = [
        {"$sort": {"chat_id": 1, "timestamp": -1}},  # Or use "_id": -1 if no createdAt
        {
            "$group": {
                "_id": "$chat_id",
                "latest": {"$first": "$$ROOT"}
            }
        },
        {"$replaceRoot": {"newRoot": "$latest"}},
        {"$sort": {"chat_id": 1}}
    ]
    newest_per_chat = list(col.aggregate(pipeline))
    for x in newest_per_chat:
        x['_id'] = str(x['_id'])
    return newest_per_chat


def read_chatids():
    return list(col.distinct("chat_id"))
