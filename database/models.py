from sqlalchemy import Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base

# Base é uma classe "mágica" da qual nossos modelos herdarão.
Base = declarative_base()

class ConversationState(Base):
    # O nome da tabela no banco de dados
    __tablename__ = "conversation_states"

    # Nossas colunas:
    # user_id será a chave primária (identificador único)
    user_id = Column(String, primary_key=True, index=True)

    # state será uma coluna do tipo JSON para armazenar nosso dicionário de estado
    # Ex: {"stage": "ordering_pizza", "order": ["Calabresa"]}
    state = Column(JSON)