import chromadb
from chromadb.config import Settings

# Local persistent DB in folder "chroma_store"
client = chromadb.PersistentClient(
    path="./chroma_store"
)

# Collections
kb_collection = client.get_or_create_collection(
    name="kb_docs",
    metadata={"hnsw:space": "cosine"}
)

incident_collection = client.get_or_create_collection(
    name="incident_docs",
    metadata={"hnsw:space": "cosine"}
)

memory_collection = client.get_or_create_collection(
    name="memory_docs",
    metadata={"hnsw:space": "cosine"}
)
