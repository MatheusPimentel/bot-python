import requests
import os
import json

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")

WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

def send_message(recipient_number: str, text: str):
    """
    Envia uma mensagem de texto para um número específico via WhatsApp Cloud API.
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_number,
        "text": {"body": text},
    }

    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Mensagem enviada com sucesso para {recipient_number}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem para o WhatsApp: {e}")
        if e.response is not None:
            print(f"Detalhes do erro: {e.response.text}")