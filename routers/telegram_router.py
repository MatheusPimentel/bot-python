from fastapi import APIRouter, Request

from core.logic import process_message
from adapters.telegram_adapter import send_message

router = APIRouter()

@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    dados = await request.json()

    try:
        chat_id = dados['message']['chat']['id']
        texto_recebido = dados['message']['text']

        # 1. Chama a lógica central
        texto_resposta = process_message(user_id=str(chat_id), message_text=texto_recebido)

        # 2. Usa o adaptador para enviar a resposta
        if texto_resposta:
            send_message(chat_id=chat_id, text=texto_resposta)

    except KeyError:
        print("Erro: Estrutura de JSON inesperada recebida do Telegram")
        pass

    return {"status": "ok"}