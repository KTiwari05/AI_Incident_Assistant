import uuid
from app.core.chroma_client import kb_collection
from app.rag.chunking import chunk_text

def ingest_document(title: str, text: str):
    chunks = chunk_text(text)

    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"title": title} for _ in chunks]

    kb_collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    return {"chunks_added": len(chunks)}
