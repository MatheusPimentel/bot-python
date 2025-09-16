# database/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# 1. IMPORTE A FERRAMENTA NECESSÁRIA
from sqlalchemy.orm.attributes import flag_modified
from .models import ConversationState

async def get_state(db: AsyncSession, user_id: str):
    result = await db.execute(select(ConversationState).filter(ConversationState.user_id == user_id))
    state = result.scalars().first()
    return state

async def create_or_update_state(db: AsyncSession, user_id: str, state_data: dict):
    existing_state = await get_state(db, user_id)

    if existing_state:
        existing_state.state = state_data
        flag_modified(existing_state, "state")
    else:
        existing_state = ConversationState(user_id=user_id, state=state_data)
        db.add(existing_state)

    await db.commit()
    await db.refresh(existing_state)
    return existing_state

async def delete_state(db: AsyncSession, user_id: str):
    state = await get_state(db, user_id)
    if state:
        await db.delete(state)
        await db.commit()
    return state