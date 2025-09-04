from fastapi import FastAPI
from contextlib import asynccontextmanager  # 1. Importe esta ferramenta
from routers import telegram_router, whatsapp_router
from database import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INFO:     Iniciando a aplicação e criando tabelas do banco de dados...")
    await database.create_db_and_tables()

    yield  # A aplicação fica "viva" e rodando aqui

    print("INFO:     Encerrando a aplicação...")

app = FastAPI(lifespan=lifespan)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Bot API is running"}


# Incluímos nossos routers normalmente
app.include_router(telegram_router.router)
app.include_router(whatsapp_router.router)