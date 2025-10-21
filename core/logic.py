# core/logic.py

import spacy
from sqlalchemy.ext.asyncio import AsyncSession
from database import crud

print("Carregando modelo de IA...")
nlp = spacy.load("model_output/model-best")
print("Modelo de IA carregado com sucesso.")

KNOWN_FLAVORS = ["calabresa", "mussarela", "quatro queijos", "frango com catupiry", "portuguesa", "marguerita"]

# --- DICIONÁRIO DE REGRAS DE PRIORIDADE ---
# Mapeia frases exatas para intenções, bypassando a IA para casos simples.
DIRECT_INTENTS = {
    "oi": "saudacao",
    "olá": "saudacao",
    "e aí": "saudacao",
    "bom dia": "saudacao",
    "boa tarde": "saudacao",
    "boa noite": "saudacao",
    "tchau": "despedida",
    "até mais": "despedida",
    "/pedido": "fazer_pedido",
    "/cancelar": "cancelar",
    "/ajuda": "ajuda",
    "/finalizar": "finalizar_pedido"  # Adicionamos uma intenção específica para /finalizar
}


async def process_message(db: AsyncSession, user_id: str, message_text: str) -> str:
    # A mensagem original, sem ser convertida para minúsculas
    original_text = message_text
    # A mensagem normalizada para a IA
    lower_text = message_text.lower()

    intent = None
    confidence = 1.0  # Confiança é 100% para regras diretas

    # 1. VERIFICA AS REGRAS DIRETAS PRIMEIRO
    if lower_text in DIRECT_INTENTS:
        intent = DIRECT_INTENTS[lower_text]
        print(f"Usuário: {user_id}, Mensagem: '{original_text}', Intenção por REGRA DIRETA: {intent}")
    else:
        # 2. SE NENHUMA REGRA, USA A IA
        doc = nlp(lower_text)
        intent = max(doc.cats, key=doc.cats.get)
        confidence = doc.cats[intent]
        print(
            f"Usuário: {user_id}, Mensagem: '{original_text}', Intenção por IA: {intent} (Confiança: {confidence:.2f})")

    user_state_record = await crud.get_state(db, user_id)
    current_state = user_state_record.state if user_state_record else {}
    stage = current_state.get("stage")

    # --- LÓGICA DE CONVERSA ---

    if stage == "ordering_pizza":
        if intent == "cancelar":
            await crud.delete_state(db, user_id)
            return "Seu pedido foi cancelado."

        if intent == "finalizar_pedido":
            order = current_state.get("order", [])
            if not order:
                return "Você ainda não adicionou nenhum sabor. Diga qual pizza você gostaria ou /cancelar."
            response = f"Pedido finalizado com sucesso! Sabores: {', '.join(order)}. Obrigado!"
            await crud.delete_state(db, user_id)
            return response

        flavors_found = [flavor for flavor in KNOWN_FLAVORS if flavor in lower_text]
        if flavors_found:
            for flavor in flavors_found:
                current_state["order"].append(flavor.capitalize())
            await crud.create_or_update_state(db, user_id, current_state)
            flavors_text = ", ".join(f"'{f.capitalize()}'" for f in flavors_found)
            return f"Sabor(es) {flavors_text} adicionado(s). Pedido atual: {', '.join(current_state['order'])}. Diga o próximo ou use /finalizar."
        else:
            return "Não encontrei um sabor de pizza conhecido nessa frase. Nosso cardápio é: Calabresa, Mussarela, etc. Você também pode /finalizar ou /cancelar."

    # --- LÓGICA DE INÍCIO DE CONVERSA ---

    if confidence < 0.7 and intent not in DIRECT_INTENTS:  # Só aplicamos o limiar se a decisão foi da IA
        return "Desculpe, não tenho certeza de como ajudar. Você gostaria de fazer um pedido?"

    if intent == "fazer_pedido":
        new_state = {"stage": "ordering_pizza", "order": []}
        await crud.create_or_update_state(db, user_id, new_state)
        return "Vamos começar seu pedido de pizza! Qual o primeiro sabor que você gostaria?"

    elif intent == "saudacao":
        return "Olá! Sou seu assistente de pedidos. Para pedir uma pizza, é só falar!"
    elif intent == "despedida":
        return "Até logo!"
    elif intent == "ajuda":
        return "Eu sou um bot de pedidos de pizza. Apenas me diga que quer um pedido para começar."
    elif intent == "cancelar":
        return "Não há nenhuma ação em andamento para cancelar."
    else:
        return "Não entendi. Para pedir uma pizza, diga 'quero fazer um pedido'."