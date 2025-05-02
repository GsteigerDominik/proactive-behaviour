import os
from datetime import datetime

import pymongo
from dotenv import load_dotenv

# SETUP
load_dotenv()
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client["proactive-behaviour"]
col = db["test"]


def insert_szenario(chat_id, szenario):
    for chat in szenario:
        insert_message(chat_id, datetime.strptime(chat['datetime'], '%Y-%m-%d %H:%M:%S'), chat['is_user'],
                       chat['message'])


def insert_message(szenario, datetime, is_user, message):
    # Define bevor usage
    col.insert_one(
        {
            "chat_id": szenario,
            "timestamp": datetime,
            "is_user": is_user,
            "message": message

        }
    )


def delete_szenario(szenario):
    query_filter = {"chat_id": szenario}
    result = col.delete_many(query_filter)


import json

# Open and read the JSON file
#chat_ids = ['szenario-01','szenario-02','szenario-03']
chat_ids = ['dominik-en']
#chat_ids = ['demo-01', 'demo-02']
for chat_id in chat_ids:
    delete_szenario(chat_id)
    with open(chat_id + '.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    #insert_szenario(chat_id, data)
