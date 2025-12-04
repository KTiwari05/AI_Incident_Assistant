from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.chat_test import router as chat_test_router
from app.api.rag_test import router as rag_test_router
from app.api.memory_test import router as memory_test_router
from app.api.chat_incident import router as chat_incident_router
from app.api.chat_general import router as chat_general_router
from app.core.db import engine, Base  # ⬅️ import engine & Base
from app.api.incidents import router as incidents_router
from app.api.metrics_llm import router as metrics_llm_router
from app.api.logs import router as logs_router


app = FastAPI(
    title="AI Incident Assistant",
    version="0.1.0",
)

# Routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(chat_test_router, prefix="/chat/test", tags=["chat-test"])
app.include_router(rag_test_router, prefix="/rag/test", tags=["rag-test"])
app.include_router(memory_test_router, prefix="/memory/test", tags=["memory-test"])
app.include_router(chat_incident_router, prefix="/chat/incident", tags=["chat-incident"])
app.include_router(chat_general_router, prefix="/chat/general", tags=["chat-general"])
app.include_router(incidents_router, prefix="/incidents", tags=["incidents"])
app.include_router(metrics_llm_router, prefix="/metrics/llm", tags=["metrics-llm"])
app.include_router(logs_router, prefix="/logs", tags=["logs"])


@app.on_event("startup")
async def on_startup():
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def root():
    return {"message": "AI Incident Assistant backend is running"}
