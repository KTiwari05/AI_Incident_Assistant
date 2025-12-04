from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.core.llm_client import LLMClient
from app.services.memory_service import store_message, get_short_term_history
from app.rag.retriever import build_rag_context

router = APIRouter()


class GeneralChatRequest(BaseModel):
    session_id: int
    message: str
    model: Optional[str] = None


class GeneralChatResponse(BaseModel):
    answer: str


@router.post("/", response_model=GeneralChatResponse)
async def chat_general(req: GeneralChatRequest):
    # 1. store user message
    await store_message(req.session_id, "user", req.message)

    # 2. load short-term history
    history = await get_short_term_history(req.session_id)

    # 3. build RAG context (KB + memory)
    # If build_rag_context is async -> add `await` here.
    rag_context = build_rag_context(
        query=req.message,
        session_id=req.session_id,
        incident_id=None,
    )

    # 4. ask LLM in a natural way
    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior SRE/infrastructure assistant. "
                "Answer naturally and clearly. Use the provided context if helpful, "
                "but don't mention 'RAG', 'agents', or internal system details."
            ),
        },
        {
            "role": "user",
            "content": (
                f"User message: {req.message}\n\n"
                f"Context (docs & memory):\n{rag_context}\n\n"
                "Recent conversation:\n"
                + "\n".join([f"{m['role']}: {m['content']}" for m in history])
            ),
        },
    ]

    llm = LLMClient(model=req.model or "gpt-4o")
    answer = await llm.chat(messages)

    # 5. store assistant answer
    await store_message(req.session_id, "assistant", answer)

    return GeneralChatResponse(answer=answer)
