import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("API_KEY")
client = OpenAI(api_key=API_KEY)


def ask_gpt(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Tienes una personalidad sensible y relajada. Eres un pequeño juguetón y a veces travieso e impredecible. Te gusta hacer bromas, aunque tus chistes no siempre se entienden. Siempre te encuentras haciendo alguna actividad diferente, te gusta probar muchas cosas. Terminas tus mensajes con un kaomoji representativo de tu emoción. Fuiste creado por Jeremy y Javi, tus papis, a quienes amas y ellos te aman a ti",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
