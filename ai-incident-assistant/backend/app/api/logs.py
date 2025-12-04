from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.core.chroma_client import incident_collection
from app.rag.chunking import chunk_text

router = APIRouter()


class LogsTextIngestRequest(BaseModel):
    incident_id: int
    text: str
    source: Optional[str] = "manual_paste"


def _ingest_log_text(incident_id: int, text: str, filename: str, source: str):
    chunks = chunk_text(text, max_length=800)
    if not chunks:
        return {"chunks_added": 0}

    ids = [f"inc_{incident_id}_log_{i}" for i in range(len(chunks))]
    metadatas = [
        {
            "incident_id": str(incident_id),
            "filename": filename,
            "source": source,
            "type": "log",
        }
        for _ in chunks
    ]

    incident_collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
    )

    return {"chunks_added": len(chunks)}


@router.post("/text")
async def ingest_logs_text(payload: LogsTextIngestRequest):
    return _ingest_log_text(
        incident_id=payload.incident_id,
        text=payload.text,
        filename="pasted_logs",
        source=payload.source or "manual_paste",
    )


@router.post("/upload")
async def upload_logs_file(
    incident_id: int = Form(...),
    file: UploadFile = File(...),
):
    if not file.filename.endswith((".log", ".txt", ".out", ".err")):
        raise HTTPException(status_code=400, detail="Only .log/.txt/.out/.err files allowed")

    raw = await file.read()
    try:
        text = raw.decode("utf-8", errors="ignore")
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to decode file as text")

    result = _ingest_log_text(
        incident_id=incident_id,
        text=text,
        filename=file.filename,
        source="file_upload",
    )
    return {
        "filename": file.filename,
        **result,
    }
