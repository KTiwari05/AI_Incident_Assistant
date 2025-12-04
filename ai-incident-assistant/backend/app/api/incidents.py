from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.db import get_db
from app.models.db_models import Incident
from app.models.schemas import IncidentCreate, IncidentOut, IncidentUpdate

router = APIRouter()


@router.get("/", response_model=List[IncidentOut])
async def list_incidents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Incident).order_by(Incident.created_at.desc()))
    incidents = result.scalars().all()
    return incidents


@router.post("/", response_model=IncidentOut)
async def create_incident(payload: IncidentCreate, db: AsyncSession = Depends(get_db)):
    inc = Incident(
        title=payload.title,
        description=payload.description,
        severity=payload.severity,
        status=payload.status,
        source="manual",
    )
    db.add(inc)
    await db.commit()
    await db.refresh(inc)
    return inc


@router.patch("/{incident_id}", response_model=IncidentOut)
async def update_incident(
    incident_id: int,
    payload: IncidentUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    inc = result.scalars().first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")

    if payload.title is not None:
        inc.title = payload.title
    if payload.description is not None:
        inc.description = payload.description
    if payload.severity is not None:
        inc.severity = payload.severity
    if payload.status is not None:
        inc.status = payload.status

    db.add(inc)
    await db.commit()
    await db.refresh(inc)
    return inc
