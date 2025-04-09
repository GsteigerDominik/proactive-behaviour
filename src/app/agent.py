from datetime import datetime

from response_formats import DecisionResponse
from util import mongodb_util, openai_util, file_util


def react(chat_id):
    print('do something')
    chat_hist = mongodb_util.read_chathistory_string(chat_id)
    should = should_answer(chat_hist)
    print('Decision: ' + str(should))
    if should.contact_user:
        response = generate_response(chat_hist)
        return response
    return None


def should_answer(chat_history):
    base_prompt = file_util.load_txt_file("./src/app/decision_prompt.txt")
    prompt = base_prompt.format(timestamp=datetime.now(), chat_history=chat_history)
    response: DecisionResponse = openai_util.gpt_query_with_response_format(prompt, DecisionResponse)
    print(f'{datetime.now()} DECISION_ENGINE: {response.contact_user}, Reasoning: {response.reasoning}')
    return response


def generate_response(chat_history):
    base_prompt = file_util.load_txt_file("./src/app/text_prompt.txt")
    prompt = base_prompt.format(timestamp=datetime.now(), chat_history=chat_history)
    response = openai_util.gpt_query(prompt)
    return response
