from fastapi import APIRouter, Request, Response
import os

from core.logic import process_message
from adapters.whatsapp_adapter import send_message

router = APIRouter()

# O token que você mesmo cria no painel da Meta para verificar seu webhook
VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN")


# Endpoint para a verificação do webhook (GET)
@router.get("/webhook/whatsapp")
async def whatsapp_verify(request: Request):
    if request.query_params.get("hub.mode") == "subscribe" and request.query_params.get(
            "hub.verify_token") == VERIFY_TOKEN:
        return Response(content=request.query_params["hub.challenge"], status_code=200)
    return Response(content="Verification failed", status_code=403)


# Endpoint para receber mensagens (POST)
@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    print(f"Webhook do WhatsApp recebido: {data}")  # Log para vermos o JSON completo

    try:
        # A estrutura do JSON da Meta é bem aninhada
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    if change.get("field") == "messages":
                        message_data = change.get("value", {}).get("messages", [{}])[0]

                        if message_data.get("type") == "text":
                            sender_id = message_data["from"]
                            message_text = message_data["text"]["body"]

                            # 1. Chama a MESMA lógica central
                            response_text = process_message(user_id=sender_id, message_text=message_text)

                            # 2. Usa o NOVO adaptador para enviar a resposta
                            if response_text:
                                send_message(recipient_number=sender_id, text=response_text)
    except Exception as e:
        print(f"Erro ao processar webhook do WhatsApp: {e}")
        pass  # Ignora erros para não quebrar o fluxo

    return Response(status_code=200)