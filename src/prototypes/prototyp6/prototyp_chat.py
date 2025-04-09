import json
import os
from datetime import datetime

import pymongo
from dotenv import load_dotenv
from openai import OpenAI

# SETUP
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
client = pymongo.MongoClient(MONGODB_CONNECTION_URL)
db = client["proactive-behaviour"]
col = db["test"]


def gpt_query(prompt):
    try:
        client = OpenAI(api_key=API_KEY, )
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt, }], model="gpt-4o-mini", )

        generated_text = chat_completion.choices[0].message.content
        return str(generated_text)
    except Exception as e:
        print(f"Error: {e}")
        return None


def load_txt_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def get_chat_hist_formated(chat_id):
    response = ""
    data = col.find({'chat_id': chat_id}).sort('timestamp')
    for x in data:
        role = "User:" if x['is_user'] else "Coach:"
        response += f"{x['timestamp']} {role}: {x['message']} \n"
    return response


def create_prompt(timestamp, chat_history, file='decision_prompt.txt'):
    base_prompt = load_txt_file(file)
    return base_prompt.format(timestamp=timestamp, chat_history=chat_history)


def create_response_if_i_should(chat_history,timestamp=datetime.now()):
    prompt = create_prompt(timestamp, chat_history)
    response = gpt_query(prompt)
    response_dict = json.loads(response)
    if response_dict['answer']:
        print('Responding...')
        prompt = create_prompt(datetime.now(), chat_history, file='prompt2.txt')
        response = gpt_query(prompt)
        print(response)
    else:
        print('No Response')


chat_history = get_chat_hist_formated("szenario_c")

for i in range(1, 10):
    create_response_if_i_should(chat_history)
