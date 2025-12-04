from fastapi import APIRouter
from pydantic import BaseModel
from app.services.memory_service import store_message, get_short_term_history, summarize_and_store_long_term

router = APIRouter()

class MsgReq(BaseModel):
    session_id: int
    role: str
    content: str


@router.post("/store")
async def store(req: MsgReq):
    await store_message(req.session_id, req.role, req.content)
    return {"status": "stored"}


@router.get("/history/{session_id}")
async def history(session_id: int):
    return await get_short_term_history(session_id)


@router.get("/summarize/{session_id}")
async def summarize(session_id: int):
    summary = await summarize_and_store_long_term(session_id)
    return {"summary": summary}
