"""Retrieval augmented generation scaffolding for the Emotional Companion."""
from __future__ import annotations

from typing import List, Sequence

from ..models import JournalEntryRead
from .vector_store import VectorStore


class RagEngine:
    """Coordinates vector retrieval and lightweight summarisation."""

    def __init__(self, vector_store: VectorStore) -> None:
        self._vector_store = vector_store

    def search(self, query: str, limit: int = 5) -> List[str]:
        return self._vector_store.search(query, limit=limit)

    def summarize(self, entries: Sequence[JournalEntryRead]) -> str:
        """Combine journal entry snippets into a tiny summary.

        In production, this method would leverage an LLM with retrieved context.
        For now it builds a deterministic string for frontend prototyping.
        """

        if not entries:
            return "No journal history available yet. Start writing to build insights!"

        latest = entries[-1]
        tag_cloud = ", ".join({tag for entry in entries for tag in entry.tags} or ["untagged"])
        return (
            "Latest emotion: "
            f"{latest.emotion.value}. "
            f"Total entries: {len(entries)}. "
            f"Tags covered: {tag_cloud}."
        )


__all__ = ["RagEngine"]
