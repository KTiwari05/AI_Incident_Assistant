from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IncidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: str = "P2"
    status: str = "Open"


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    status: Optional[str] = None


class IncidentOut(IncidentBase):
    id: int
    source: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
