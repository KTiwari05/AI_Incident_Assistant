from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_db
from app.models.db_models import LLMCall

router = APIRouter()


@router.get("/")
async def llm_metrics(db: AsyncSession = Depends(get_db)):
    # overall metrics
    q_all = select(
        func.count(LLMCall.id),
        func.avg(LLMCall.latency_ms),
        func.sum(LLMCall.prompt_chars),
        func.sum(LLMCall.completion_chars),
    )
    total_calls, avg_latency, total_prompt_chars, total_completion_chars = (
        await db.execute(q_all)
    ).one()

    # per-model metrics
    q_per_model = select(
        LLMCall.model,
        func.count(LLMCall.id),
        func.avg(LLMCall.latency_ms),
    ).group_by(LLMCall.model)

    rows = (await db.execute(q_per_model)).all()
    per_model = [
        {
            "model": r[0],
            "count": r[1],
            "avg_latency_ms": float(r[2]) if r[2] is not None else None,
        }
        for r in rows
    ]

    return {
        "total_calls": total_calls or 0,
        "avg_latency_ms": float(avg_latency) if avg_latency is not None else None,
        "total_prompt_chars": int(total_prompt_chars or 0),
        "total_completion_chars": int(total_completion_chars or 0),
        "per_model": per_model,
    }
