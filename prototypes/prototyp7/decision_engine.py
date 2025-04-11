import json
from datetime import datetime

from data.prototyp7.chatgpt_adapter import gpt_query, gpt_query_with_response_format
from data.prototyp7.response_formats import DecisionResponse


def load_txt_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def should_answer(chat_history):
    base_prompt = load_txt_file("decision_prompt.txt")
    prompt = base_prompt.format(timestamp=datetime.now(), chat_history=chat_history)
    response:DecisionResponse = gpt_query_with_response_format(prompt,DecisionResponse)
    print(f'{datetime.now()} DECISION_ENGINE: {response.contact_user}, Reasoning: {response.reasoning}')
    return response
