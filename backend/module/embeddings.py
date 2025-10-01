import os
from typing import List

from qdrant_client import AsyncQdrantClient, models


def create_qdrant():
    QDRANT_URL = os.environ.get("QDRANT_URL")
    if not QDRANT_URL:
        raise ValueError("Setup your qdrant client")
    return AsyncQdrantClient(path=QDRANT_URL)


def chunk_string(text, max_words=500, overlap_words=100):
    words = text.split()
    docs = []
    pointer = 0
    while pointer < len(words):
        start = max(0, pointer - overlap_words)
        end = pointer + max_words
        docs.append(" ".join(words[start:end]))
        pointer += max_words
    return docs


async def create_collection(client: AsyncQdrantClient, name: str, size: int):
    await client.create_collection(
        collection_name=name,
        vectors_config=models.VectorParams(size=size, distance=models.Distance.COSINE),
    )


async def insert_vector(
    client: AsyncQdrantClient, collection_name: str, documents: List[str]
):
    await client.add(collection_name=collection_name, documents=documents)


async def search(client: AsyncQdrantClient, collection_name: str, query: str):
    # Search for nearest neighbors
    search_result = await client.query(
        collection_name=collection_name,
        query_text=query,
        limit=20,
    )

    return search_result


async def embbed_book(book, client: AsyncQdrantClient):
    content = book.get_all_chap()
    chunks = chunk_string(content)
    collections = await client.get_collections()
    all_col = collections.collections
    exists = any(c.name == book.id for c in all_col)
    if not exists:
        await client.create_collection(
            collection_name=book.id,
            vectors_config={
                "fast-bge-small-en": models.VectorParams(
                    size=384,
                    distance=models.Distance.COSINE,
                )
            },
        )
    await client.add(collection_name=book.id, documents=chunks)
