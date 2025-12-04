from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.services.memory_service import (
    store_message,
    get_short_term_history,
    summarize_and_store_long_term,
)
from app.rag.retriever import build_rag_context
from app.agents.orchestrator import Orchestrator

router = APIRouter()


class IncidentChatRequest(BaseModel):
    session_id: int
    incident_id: Optional[int] = None
    message: str
    logs: Optional[str] = None
    metrics: Optional[str] = None
    model: Optional[str] = None   # allow override if you want later


class IncidentChatResponse(BaseModel):
    answer: str
    agents_output: dict


@router.post("/", response_model=IncidentChatResponse)
async def chat_incident(req: IncidentChatRequest):
    # 1. Store user message in short-term memory
    await store_message(req.session_id, "user", req.message)

    # 2. Load short-term history
    history = await get_short_term_history(req.session_id)

    # 3. Build RAG context (KB + incidents + long-term memory)
    rag_context = build_rag_context(
        query=req.message,
        session_id=req.session_id,
        incident_id=req.incident_id,
    )

    # 4. Build context for agents
    context = {
        "user_query": req.message,
        "history": history,
        "rag_context": rag_context,
        "logs": req.logs or "",
        "monitoring": req.metrics or "",
        "incident_id": req.incident_id,
        "session_id": req.session_id,
    }

    # 5. Run multi-agent orchestrator
    orchestrator = Orchestrator(model=req.model or "gpt-4o")
    result = await orchestrator.handle(context)

    final_answer = result["final_answer"]["final_answer"]

    # 6. Store assistant message
    await store_message(req.session_id, "assistant", final_answer)

    # 7. Optionally refresh long-term memory summary every turn (simple but fine for hackathon)
    await summarize_and_store_long_term(req.session_id)

    return IncidentChatResponse(
        answer=final_answer,
        agents_output=result,
    )
