from openai import OpenAI

from app import env


def gpt_query(prompt):
    try:
        client = OpenAI(api_key=env.OPENAI_API_KEY, )
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt, }],
            model="gpt-4o-mini",
            temperature=1)

        generated_text = chat_completion.choices[0].message.content
        return str(generated_text)
    except Exception as e:
        print(f"Error: {e}")
        return None


def gpt_query_with_response_format(prompt, response_format):
    try:
        client = OpenAI(api_key=env.OPENAI_API_KEY, )
        chat_completion = client.beta.chat.completions.parse(
            messages=[{"role": "user", "content": prompt, }], model="gpt-4o-mini",
            response_format=response_format,
            temperature=0.8)
        return chat_completion.choices[0].message.parsed
    except Exception as e:
        print(f"Error: {e}")
        return None


def load_txt_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content
