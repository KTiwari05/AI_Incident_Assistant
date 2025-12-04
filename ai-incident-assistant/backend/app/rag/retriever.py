from typing import Optional
from app.core.chroma_client import kb_collection, incident_collection, memory_collection


def _retrieve_from_collection(collection, query: str, top_k: int, where: Optional[dict] = None):
    if collection is None:
        return []

    if where:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            where=where,
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
        )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    formatted = []
    for d, m in zip(docs, metas):
        m = m or {}
        formatted.append({
            "content": d,
            "title": m.get("title"),
            "meta": m,
        })
    return formatted


def build_rag_context(query: str, session_id: Optional[int] = None, incident_id: Optional[int] = None) -> str:
    kb_hits = _retrieve_from_collection(kb_collection, query, 4)

    if incident_id is not None:
        where = {"incident_id": str(incident_id)}
    else:
        where = None

    incident_hits = _retrieve_from_collection(incident_collection, query, 4, where=where)
    memory_hits = _retrieve_from_collection(memory_collection, query, 3)

    parts: list[str] = []

    if kb_hits:
        parts.append("### Documentation / Runbooks\n")
        for h in kb_hits:
            parts.append(f"[{h['title'] or 'KB Doc'}]: {h['content']}\n")

    if incident_hits:
        parts.append("\n### Incident-Specific Logs & History\n")
        for h in incident_hits:
            meta = h["meta"]
            src = meta.get("source", "unknown")
            fname = meta.get("filename", "logs")
            parts.append(f"- ({src}, {fname}): {h['content']}\n")

    if memory_hits:
        parts.append("\n### Long-Term Conversation Memory\n")
        for h in memory_hits:
            parts.append(f"- {h['content']}\n")

    if not parts:
        return "No relevant context found in KB, incidents, or memory."

    return "\n".join(parts)
