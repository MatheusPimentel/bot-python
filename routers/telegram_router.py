from fastapi import APIRouter, Request

from core.logic import process_message
from adapters.telegram_adapter import send_message
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db

router = APIRouter()

@router.post("/webhook/telegram")
# A assinatura da função muda para receber a dependência 'db'
async def telegram_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    dados = await request.json()
    try:
        chat_id = dados['message']['chat']['id']
        texto_recebido = dados['message']['text']
        # Passamos a sessão 'db' para a função de lógica
        texto_resposta = await process_message(db=db, user_id=str(chat_id), message_text=texto_recebido)
        if texto_resposta:
            send_message(chat_id=chat_id, text=texto_resposta)

    except KeyError:
        print("Erro: Estrutura de JSON inesperada recebida do Telegram")
        pass

    return {"status": "ok"}