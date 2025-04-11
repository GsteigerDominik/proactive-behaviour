import time
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


def create_prompt(szenario, timestamp):
    return (
            "Today is " + timestamp + ".\n\n You are the Coach in this conversation."
                                      "Based on the following situation, decide whether we should reach out to the user. "
                                      "If there are incomplete conversations between the coach and the user we should complete it ('Yes')."
                                      "If the user has been recently active, adjusting their goal, or showing self-motivation, do not reach out ('No'). "
                                      "If there are signs of struggle, hesitation or long inactivity, reaching out may be helpful ('Yes'). "
                                      "Briefly explain your reasoning before providing your final decision (Yes/No). "
                                      "Most importantly, you must consider the user's requests:\n"
                                      "- If the user has explicitly requested contact **after** a specific date, do not contact them before that date.\n"
                                      "- If today is before that date, do **not** contact them.\n"
                                      "- If today is on or after that date, you should likely reach out.\n\n"
                                      "- Think in steps, first identify which date and time is today, then identify the requested datetime, decide if the datetime is already due."
                                      "You should behave like a regular human, soo you probably wont contact users in the night."
                                      "Your goal is to be supportive without putting pressure on the user or messaging him over and over again.\n\n"
                                      "Scenario: " + szenario + "\n\n"
                                                                "The output should contain only Yes or No, and a really short reasoning")


import datetime


def job(szenario):
    currentDateAndTime = datetime.datetime.now()
    response = gpt_query(create_prompt(szenario, str(currentDateAndTime)))
    print("Szenario:",currentDateAndTime, response)


szenario = load_txt_file('szenario_c.txt')

while 1:
    job(szenario)
    time.sleep(1)