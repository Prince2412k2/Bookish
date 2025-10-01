import clients
from qdrant_client import AsyncQdrantClient


async def get_qdrant() -> AsyncQdrantClient:
    if clients.qdrant is None:
        raise RuntimeError("Qdrant not initialized")
    return clients.qdrant
