from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    incident_id = Column(Integer, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String(20))   # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(10), default="P2")  # P1/P2/P3
    status = Column(String(20), default="Open")  # Open/Investigating/Resolved
    source = Column(String(50), default="manual")  # "manual", "monitoring", etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LLMCall(Base):
    __tablename__ = "llm_calls"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    latency_ms = Column(Float, nullable=False)
    prompt_chars = Column(Integer, nullable=False)
    completion_chars = Column(Integer, nullable=False)
    success = Column(Boolean, default=True)
    error = Column(Text, nullable=True)