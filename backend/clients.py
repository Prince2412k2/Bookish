from qdrant_client import AsyncQdrantClient

# Declare globals (not initialized yet)
qdrant: AsyncQdrantClient | None = None
