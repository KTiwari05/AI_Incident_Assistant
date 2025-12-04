from fastapi import APIRouter
from pydantic import BaseModel
from app.rag.ingest import ingest_document
from app.rag.retriever import build_rag_context

router = APIRouter()

class IngestRequest(BaseModel):
    title: str
    text: str

class QueryRequest(BaseModel):
    query: str


@router.post("/ingest")
def ingest(req: IngestRequest):
    return ingest_document(req.title, req.text)


@router.post("/query")
def query(req: QueryRequest):
    context = build_rag_context(req.query)
    return {"context": context}
