import time
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

DB_PATH = Path(__file__).parent.parent.parent / "data" / "chroma_db"


class LongTermMemory:
    def __init__(self, user_name: str = "default"):
        self._client = chromadb.PersistentClient(path=str(DB_PATH))
        collection_name = f"user_{user_name.lower().replace(' ', '_')}"
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=DefaultEmbeddingFunction(),
        )

    def store(self, text: str, metadata: dict | None = None) -> None:
        self._collection.add(
            documents=[text],
            ids=[f"mem_{int(time.time() * 1000)}"],
            metadatas=[metadata or {}],
        )

    def retrieve(self, query: str, n_results: int = 3) -> list[str]:
        count = self._collection.count()
        if count == 0:
            return []
        results = self._collection.query(
            query_texts=[query],
            n_results=min(n_results, count),
        )
        return results["documents"][0] if results["documents"] else []
