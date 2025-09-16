from sqlalchemy.ext.asyncio import AsyncSession
from database import crud

# O dicionário em memória é removido. O banco de dados é nossa nova fonte da verdade.

async def process_message(db: AsyncSession, user_id: str, message_text: str) -> str:
    """
    Processa a mensagem com base no estado salvo no BANCO DE DADOS.
    Note que a função agora é 'async'.
    """
    print(f"Processando para o usuário: {user_id}")

    # Lemos o estado do usuário do banco de dados
    user_state_record = await crud.get_state(db, user_id)
    current_state = user_state_record.state if user_state_record else {}
    stage = current_state.get("stage")

    message_text = message_text.lower()

    # --- Lógica de Conversa Baseada em Estado ---

    if stage == "ordering_pizza":
        if "/finalizar" in message_text:
            order = current_state.get("order", [])
            response = f"Pedido finalizado com sucesso! Sabores: {', '.join(order)}. Obrigado!"
            # Apagamos o estado do usuário do banco de dados
            await crud.delete_state(db, user_id)
            return response
        else:
            current_state["order"].append(message_text.capitalize())
            # Atualizamos o estado no banco de dados
            await crud.create_or_update_state(db, user_id, current_state)
            return f"Sabor '{message_text.capitalize()}' adicionado. Para adicionar outro sabor, me diga qual é. Ou digite /finalizar para encerrar."

    # --- Comandos Principais ---

    if "/pedido" in message_text:
        new_state = {
            "stage": "ordering_pizza",
            "order": []
        }
        # Criamos o estado inicial no banco de dados
        await crud.create_or_update_state(db, user_id, new_state)
        return "Vamos começar seu pedido de pizza! Qual o primeiro sabor que você gostaria?"

    elif "/cancelar" in message_text:
        if user_state_record:
            await crud.delete_state(db, user_id)
            return "Ação cancelada."
        else:
            return "Não há nenhuma ação em andamento para cancelar."

    else:
        return "Olá! Use /pedido para iniciar um pedido de pizza ou /ajuda para mais informações."