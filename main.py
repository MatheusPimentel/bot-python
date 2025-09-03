from fastapi import FastAPI
from routers import telegram_router, whatsapp_router

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Bot API is running"}

app.include_router(telegram_router.router)
app.include_router(whatsapp_router.router)