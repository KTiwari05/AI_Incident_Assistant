from sqlalchemy import select
from app.models.db_models import Message
from app.core.chroma_client import memory_collection
from app.core.llm_client import LLMClient
from app.core.db import async_session
from typing import List


MAX_HISTORY = 10  # short-term memory window


async def store_message(session_id: int, role: str, content: str):
    async with async_session() as db:
        msg = Message(
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(msg)
        await db.commit()


async def get_short_term_history(session_id: int) -> List[dict]:
    async with async_session() as db:
        q = select(Message).where(Message.session_id == session_id).order_by(Message.created_at.desc()).limit(MAX_HISTORY)
        rows = (await db.execute(q)).scalars().all()

        history = [
            {"role": m.role, "content": m.content}
            for m in reversed(rows)   # chronological
        ]
        return history


async def summarize_and_store_long_term(session_id: int):
    """Summarize the short-term memory and store as vector in Chroma."""
    history = await get_short_term_history(session_id)

    text = "\n".join([f"{h['role'].upper()}: {h['content']}" for h in history])

    llm = LLMClient()
    summary = await llm.chat([
        {"role": "system", "content": "Summarize this conversation briefly."},
        {"role": "user", "content": text}
    ])

    memory_collection.add(
        ids=[f"mem_{session_id}"],
        documents=[summary],
        metadatas=[{"session_id": session_id}]
    )

    return summary
