import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

class ContactUserResponse(BaseModel):
    contactUser: bool
    reasoning: str

def gpt_query(prompt):
    try:
        client = OpenAI(api_key=API_KEY, )
        chat_completion = client.beta.chat.completions.parse(
            messages=[{"role": "user", "content": prompt, }], model="gpt-4o-mini",response_format=ContactUserResponse )
        generated_text = chat_completion.choices[0].message.parsed
        return str(generated_text)
    except Exception as e:
        print(f"Error: {e}")
        return None


def load_txt_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


user_interaction_history = load_txt_file('s2.txt')


LONG_TERM_STATUS_PROMPT = (
    "Analyze the user's progress and engagement based on the provided interactions. "
    "Categorize the user into one of the following states:\n"
    "- 'Engaged & Motivated': User is responding actively and progressing towards their goal.\n"
    "- 'Some Struggles but Engaged': User has had setbacks but remains responsive and interested.\n"
    "- 'Falling Off but Responsive': User is skipping activities and showing low motivation, but still replies occasionally.\n"
    "- 'Unresponsive / Lost Interest': User has not responded for a significant time or has expressed a loss of interest.\n\n"
    "Provide reasoning before giving the final category.\n\n"
    "User interactions:\n"+user_interaction_history+"\n\n"
    "Final Category: "
)

MOMENTARY_DECISION_PROMPT = (
    "DateTime right now: 04.04.2025 23:40"
    "Based on the user's status (Some Struggles but Engaged), determine whether reaching out right now is the best approach. "
    "Consider the following:\n"
    "- If the user is 'Engaged & Motivated', avoid unnecessary messages.\n"
    "- If the user is 'Some Struggles but Engaged', reach out only if they have not responded in a while.\n"
    "- If the user is 'Falling Off but Responsive', offer encouragement at a natural moment.\n"
    "- If the user is 'Unresponsive / Lost Interest', determine whether a final check-in is appropriate.\n\n"
    "Additionally, evaluate the timing:\n"
    "- Avoid reaching out too soon after a previous check-in.\n"
    "- If the user recently ignored a message, consider waiting longer.\n"
    "- Ensure the message feels supportive rather than pressuring.\n\n"
    "Most importantly, you must consider the user's requests:\n"
    "- If the user has explicitly requested contact **after** a specific date, do not contact them before that date.\n"
    "- Today's date is 04.04.2025. Determine what 'after next Tuesday' means based on today's date.\n"
    "- If today is before that date, do **not** contact them.\n"
    "- If today is on or after that date, you should likely reach out.\n\n"
    "User's latest interaction:\n"+user_interaction_history+"\n\n"
    "Final Decision (Yes/No) and reasoning: "
)

response = gpt_query(MOMENTARY_DECISION_PROMPT)
print(response)