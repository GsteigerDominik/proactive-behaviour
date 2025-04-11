import os

import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def should_contact_user(chat_history, bot_mission):
    """
    Uses ChatGPT API to decide if the bot should contact the user.
    """

    prompt = f"""
    You are an intelligent assistant. Your mission is: {bot_mission}

    Here is the recent chat history:
    {chat_history}

    Decide whether the bot should proactively contact the user.
    Respond in JSON format with the following structure:
    {{
        "contact_user": true/false,
        "reason": "Brief explanation"
    }}
    """

    client = OpenAI(api_key=OPENAI_API_KEY, )
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Use GPT-4-turbo for efficiency
        messages=[{"role": "system", "content": "You are an AI assistant making decisions."},
                  {"role": "user", "content": prompt}],
        temperature=0.2  # Keep it deterministic
    )

    decision = response["choices"][0]["message"]["content"]
    return decision

# Example chat history
chat = """
User: I need help with my goal tracking.
Bot: Sure! What exactly are you struggling with?
User: I don't know if I'm making progress.
Bot: Let’s review your recent progress. You have completed 3 out of 5 tasks this week.
"""

# Call the function
decision = should_contact_user(chat, "Help the user stay engaged and on track with their goals.")
print(decision)
