from datetime import datetime

from data.prototyp7.chatgpt_adapter import gpt_query


def load_txt_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def generate_response(chat_history):
    base_prompt = load_txt_file("text_prompt.txt")
    prompt = base_prompt.format(timestamp=datetime.now(), chat_history=chat_history)
    response = gpt_query(prompt)
    return response
