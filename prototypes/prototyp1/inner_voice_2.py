import os

import openai
import time

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI(api_key=API_KEY)

# Kreativer Kopf - Erzeugt Ideen
kreativer_kopf_prompt = """
Du bist kreativ, voller Ideen und liebst es, Neues auszuprobieren.
Du schlägst Vorschläge vor, die spannend, innovativ oder unterhaltsam sind.
Antwortformat: Nur der Vorschlag, keine Einleitung oder Erklärung.
"""

# Vernunft - Bewertet Ideen kritisch
vernunft_prompt = """
Du bist rational, kritisch und prüfst Vorschläge auf Sinnhaftigkeit, Nutzen und Machbarkeit.
Du entscheidest klar, ob eine Idee akzeptabel ist oder nicht.

Antwortformat:
- Falls die Idee gut ist: "AKZEPTIERT: [kurze Begründung]"
- Falls die Idee schlecht ist: "ABGELEHNT: [kurze Begründung]"

Antworte ausschließlich in diesem Format, ohne zusätzlichen Text.
"""

def chat(role_prompt, message):
    """Kommuniziert mit OpenAI API basierend auf dem gegebenen Prompt."""
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": role_prompt},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def interner_dialog():
    """Kreativer Kopf schlägt etwas vor, Vernunft bewertet es, Entscheidung wird getroffen."""
    for _ in range(3):  # Maximal 3 Runden
        idee = chat(kreativer_kopf_prompt, "Gib mir eine interessante Idee, die ich umsetzen könnte.")
        print(f"🧠 Kreativer Kopf: {idee}")

        bewertung = chat(vernunft_prompt, f"Bewerte diese Idee: {idee}")
        print(f"⚖️ Vernunft: {bewertung}")

        if bewertung.startswith("AKZEPTIERT"):
            print(f"✅ Die Idee wird umgesetzt: {idee}")
            return idee  # Idee wird umgesetzt

    print("🚫 Keine passende Idee gefunden.")
    return None  # Keine Idee wird umgesetzt

# Testlauf
interner_dialog()
