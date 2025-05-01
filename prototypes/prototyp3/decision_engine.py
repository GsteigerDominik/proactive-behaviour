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
                                    "You should behave like a regular human, soo you probably wont contact users in the night."
                                    "Your goal is to be supportive without putting pressure on the user or messaging him over and over again.\n\n"
                                    "Scenario: " + szenario + "\n\n"
                                    "The output should contain only Yes or No, and a really short reasoning")


szenario = load_txt_file('s1.txt')
response = gpt_query(create_prompt(szenario, "Sunday 17.03.25 18:10"))
print("Szenario 1: Sunday 17.03.25 18:10", response)

response = gpt_query(create_prompt(szenario, "Sunday 17.03.25 18:15"))
print("Szenario 1: Sunday 17.03.25 18:15", response)

response = gpt_query(create_prompt(szenario, "Sunday 17.03.25 18:20"))
print("Szenario 1: Sunday 17.03.25 18:20", response)

response = gpt_query(create_prompt(szenario, "Sunday 17.03.25 18:30"))
print("Szenario 1: Sunday 17.03.25 18:30", response)

szenario = load_txt_file('s2.txt')
response = gpt_query(create_prompt(szenario, "Sunday 17.03.25 18:30"))
print("Szenario 2: Sunday 17.03.25 18:30", response)

response = gpt_query(create_prompt(szenario, "Monday 18.03.25 08:30"))
print("Szenario 2: Monday 18.03.25 08:30", response)

response = gpt_query(create_prompt(szenario, "Monday 18.03.25 12:30"))
print("Szenario 2: Monday 18.03.25 12:30", response)

response = gpt_query(create_prompt(szenario, "Monday 18.03.25 15:30"))
print("Szenario 2: Monday 18.03.25 15:30", response)

response = gpt_query(create_prompt(szenario, "Monday 18.03.25 16:50"))
print("Szenario 2: Monday 18.03.25 16:50", response)

response = gpt_query(create_prompt(szenario, "Monday 18.03.25 17:00"))
print("Szenario 2: Monday 18.03.25 17:00", response)

response = gpt_query(create_prompt(szenario, "Monday 18.03.25 17:05"))
print("Szenario 2: Monday 18.03.25 17:05", response)