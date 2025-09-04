import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base # Importamos a Base dos nossos modelos

PG_USER = os.environ.get("POSTGRES_USER")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
PG_HOST = os.environ.get("POSTGRES_HOST")
PG_PORT = os.environ.get("POSTGRES_PORT")
PG_DB = os.environ.get("POSTGRES_DB")

DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

# Criamos o "motor" assíncrono do SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Criamos uma classe de Sessão que será usada para interagir com o banco
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def create_db_and_tables():
    # Esta função cria a tabela no banco de dados se ela não existir
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)