from datetime import datetime

from app import response_formats
from app.util import mongodb_util, openai_util, file_util


def react(chat_id):
    chat_hist = mongodb_util.read_chathistory_string(chat_id)
    should = should_answer(chat_hist)
    print(f'{chat_id} : DECISION {should.contact_user}, {should.reasoning}')
    if should.contact_user:
        response = generate_response(chat_hist)
        print(f'{chat_id} : MESSAGE {response}')
        return response
    return None


def should_answer(chat_history):
    base_prompt = file_util.load_txt_file("./app/decision_prompt.txt")
    prompt = base_prompt.format(timestamp=datetime.now(), chat_history=chat_history)
    response: response_formats.DecisionResponse = openai_util.gpt_query_with_response_format(prompt, response_formats.DecisionResponse)
    return response


def generate_response(chat_history):
    base_prompt = file_util.load_txt_file("./app/text_prompt.txt")
    prompt = base_prompt.format(timestamp=datetime.now(), chat_history=chat_history)
    response = openai_util.gpt_query(prompt)
    return response
