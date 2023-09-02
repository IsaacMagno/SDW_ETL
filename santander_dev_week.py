import pandas as pd
import requests
import json
import openai

OPENAI_API_KEY = "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"
SDW_2023_API_URL = "https://sdw-2023-prd.up.railway.app"

df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()

openai.api_key = OPENAI_API_KEY


def get_user(id):
    response = requests.get(f'{SDW_2023_API_URL}/users/{id}')
    return response.json() if response.status_code == 200 else None


users = [user for id in user_ids if (user := get_user(id)) is not None]


def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
              "role": "system",
              "content": "Você é um especialista em markting bancário."
            },
            {
                "role": "user",
                "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres, elabore respostas criativas para cada usuario)"
            }
        ]
    )

    return completion.choices[0].message.content.strip('\"')


for user in users:
    news = generate_ai_news(user)
    user['news'].append({
        "description": news
    })


def update_user(user):
    response = requests.put(
        f"{SDW_2023_API_URL}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False


for user in users:
    success = update_user(user)
    print(f"User {user['name']} updated? {success}")
