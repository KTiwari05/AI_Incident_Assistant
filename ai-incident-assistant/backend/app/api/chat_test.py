from fastapi import APIRouter
from pydantic import BaseModel
from app.core.llm_client import LLMClient

router = APIRouter()

class ChatTestRequest(BaseModel):
    message: str
    model: str | None = None

@router.post("/")
async def chat_test(req: ChatTestRequest):
    llm = LLMClient(model=req.model)
    response = await llm.chat([
        {"role": "system", "content": "You are a test assistant."},
        {"role": "user", "content": req.message}
    ])
    return {"response": response}
