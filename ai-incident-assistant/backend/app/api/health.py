# app/api/health.py
from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "ai-incident-assistant",
        "timestamp": int(time.time()),
    }
