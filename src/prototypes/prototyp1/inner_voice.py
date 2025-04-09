import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")


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


OBSERVER_PROMPT = 'Analyze the conversation so far. What is the users emotional state? What conversational cues suggest potential concerns or unresolved issues?'
MOTIVATOR_PROMPT = 'Given the users emotional state and conversational cues, what action aligns with my goal of being helpful, engaging, and proactive?'
CRITIC_PROMPT = 'Would this action be useful? Would it be natural in the current conversational context? If not, what alternative action should be considered?'
EXECUTER_PROMPT = 'Based on the approved action, craft a conversational response that feels natural and aligns with the user’s needs.'
szenario = load_txt_file('s1.txt')
observer_response = gpt_query(
    OBSERVER_PROMPT + ' Conversation: ' + szenario + ' \nAnswer shortly (1 sentences)!')
motivator_response = gpt_query(
    MOTIVATOR_PROMPT + ' Conversational cues and motivational state: '+ ' Conversation: '  + observer_response + ' \nAnswer shortly (1 sentences)!')
print(motivator_response)
