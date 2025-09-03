user_states = {}

def process_message(user_id: str, message_text: str) -> str:
    """
    Processa a mensagem recebida e retorna o texto da resposta,
    agora com base no estado atual da conversa do usuário.
    """
    print(f"Estado atual dos usuários: {user_states}")  # Log para vermos o que está acontecendo

    # Verifica se o usuário já tem um estado de conversa
    current_state = user_states.get(user_id, {})
    stage = current_state.get("stage")

    message_text = message_text.lower()

    # --- Lógica de Conversa Baseada em Estado ---

    # Se o usuário está no meio de um pedido de pizza
    if stage == "ordering_pizza":
        # Finaliza o pedido
        if "/finalizar" in message_text:
            order = current_state.get("order", [])
            response = f"Pedido finalizado com sucesso! Sabores: {', '.join(order)}. Obrigado!"
            # Limpa o estado do usuário para que ele possa começar de novo
            del user_states[user_id]
            return response
        # Adiciona mais um sabor
        else:
            current_state["order"].append(message_text.capitalize())
            user_states[user_id] = current_state
            return f"Sabor '{message_text.capitalize()}' adicionado. Para adicionar outro sabor, me diga qual é. Ou digite /finalizar para encerrar."

    # --- Comandos Principais (Quando não há uma conversa ativa) ---

    if "/pedido" in message_text:
        # Inicia o estado de pedido para este usuário
        user_states[user_id] = {
            "stage": "ordering_pizza",
            "order": []
        }
        return "Vamos começar seu pedido de pizza! Qual o primeiro sabor que você gostaria?"

    elif "/ajuda" in message_text:
        return "Eu sou um bot de pedidos de pizza. Use o comando /pedido para começar."

    elif "/cancelar" in message_text:
        if user_id in user_states:
            del user_states[user_id]
            return "Ação cancelada."
        else:
            return "Não há nenhuma ação em andamento para cancelar."

    else:
        return "Olá! Use /pedido para iniciar um pedido de pizza ou /ajuda para mais informações."