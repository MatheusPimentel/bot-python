# adapters/telegram_adapter.py

import requests
import os  # Usaremos para pegar o token de forma mais segura

# É uma excelente prática carregar configurações sensíveis de variáveis de ambiente
# Falaremos mais sobre isso no Módulo de Boas Práticas!
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"


def send_message(chat_id: int, text: str):
    """
    Envia uma mensagem de texto para um chat específico no Telegram.
    """
    url = f"{TELEGRAM_API_URL}sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        # Lança uma exceção se a resposta da API for um erro (4xx ou 5xx)
        response.raise_for_status()
        print(f"Mensagem enviada com sucesso para o chat_id: {chat_id}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem para o Telegram: {e}")