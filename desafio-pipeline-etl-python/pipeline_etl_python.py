import csv

with open('C:\Python\challenger-santander-dev-week-2023\desafio-pipeline-etl-python\SDW2023.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

nome = "Extract"
print(nome.center(100, '#'))

import pandas as pd

df = pd.read_csv('C:\Python\challenger-santander-dev-week-2023\desafio-pipeline-etl-python\SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

import requests
import json

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

nome = "Transform"
print(nome.center(100, '#'))

# !pip install openai

openai_api_key = 'Insira aqui'

import openai

openai.api_key = openai_api_key

nome = "Load"
print(nome.center(100, '#'))

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
      {
          "role": "system",
          "content": "Olá. Preciso que você seja um especialista em marketing bancário da Santander."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos para os seus clientes. (máximo de 150 caracteres)"
      }
    ]
  )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })

  def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")
