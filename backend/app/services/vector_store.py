"""In-memory vector store approximation for journaling content."""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from ..models import JournalEntryRead


@dataclass
class EmbeddedDocument:
    entry_id: str
    embedding: Tuple[float, ...]


class VectorStore:
    """Naïve vector index built from bag-of-words scoring.

    The implementation is intentionally lightweight so it can run without any
    third-party dependencies inside this prototype. Each entry is embedded using
    a simple character-level frequency vector, which allows for deterministic
    similarity scoring that mirrors the contract of real vector databases.
    """

    def __init__(self) -> None:
        self._index: Dict[str, EmbeddedDocument] = {}

    def index(self, entry: JournalEntryRead) -> None:
        self._index[entry.entry_id] = EmbeddedDocument(
            entry_id=entry.entry_id,
            embedding=self._embed(entry.content),
        )

    def search(self, query: str, limit: int = 5) -> List[str]:
        query_embedding = self._embed(query)
        scores = [
            (self._cosine_similarity(query_embedding, doc.embedding), doc.entry_id)
            for doc in self._index.values()
        ]
        scores.sort(reverse=True)
        return [entry_id for _, entry_id in scores[:limit]]

    def _embed(self, text: str, dimensions: int = 32) -> Tuple[float, ...]:
        vector = [0.0] * dimensions
        for index, char in enumerate(text.lower()):
            vector[index % dimensions] += float(ord(char))
        norm = math.sqrt(sum(value ** 2 for value in vector)) or 1.0
        return tuple(value / norm for value in vector)

    @staticmethod
    def _cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
        return sum(x * y for x, y in zip(a, b))


__all__ = ["VectorStore", "EmbeddedDocument"]
