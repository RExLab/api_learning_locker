from flask import Flask, jsonify
from dateutil.parser import parse
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    # Configurações da sua conta no Learning Locker
    learning_locker_url = 'https://learninglocker/data/xAPI/statements/' #exemplo de URL, substituir pelo endereço do Learning Locker
    username = ''
    password = ''
    credentials = f'{username}:{password}'
    token = base64.b64encode(credentials.encode()).decode()

    # Parâmetros da consulta
   
    # Construir a consulta xAPI
    query = {
        'since': '2023-09-28T01:01:00.450Z"',
        'until': '2023-09-28T02:01:25.528Z'
    }

    # Fazer a solicitação GET para obter declarações
    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json',
        'X-Experience-API-Version': '1.0'
    }

    try:
        response = requests.get(learning_locker_url, headers=headers,  verify=False)
        response.raise_for_status()  # Lança uma exceção se a solicitação não for bem-sucedida
        statements = response.json()
        statements_array = []
        actor_mbox = "john doe"
        start_date = '2023-09-28T01:01:00.450Z'
        end_date = '2023-09-28T02:01:25.528Z'
        filtered_statements = [statement for statement in statements['statements'] if statement.get('actor', {}).get('name', '') == actor_mbox and parse(start_date) <= parse(statement.get('timestamp', '')) <= parse(end_date)]
        for statement in statements['statements']:
            statements_array.append(statement)
        return jsonify(statements)
    except requests.exceptions.RequestException as e:
        return f'Erro ao recuperar declarações do Learning Locker: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
