"""FastAPI application exposing journaling, emotion tracking, and RAG stubs."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import EmotionLabel, JournalEntryCreate, JournalEntryRead
from .services.integrations import IntegrationManager
from .services.rag import RagEngine
from .services.vector_store import VectorStore

app = FastAPI(title="Emotional Companion API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class JournalRepository:
    """In-memory persistence layer for journal entries.

    The repository mirrors a minimal database and can be replaced with a real
    database implementation later on. Identifiers are generated using a
    timestamp-based approach for determinism inside this prototype.
    """

    def __init__(self) -> None:
        self._entries: Dict[str, JournalEntryRead] = {}

    def list_entries(self) -> List[JournalEntryRead]:
        return list(sorted(self._entries.values(), key=lambda e: e.created_at))

    def get(self, entry_id: str) -> JournalEntryRead:
        try:
            return self._entries[entry_id]
        except KeyError as exc:  # pragma: no cover - defensive path
            raise HTTPException(status_code=404, detail="Entry not found") from exc

    def add(self, entry: JournalEntryCreate) -> JournalEntryRead:
        entry_id = entry.entry_id or f"entry-{int(datetime.utcnow().timestamp() * 1000)}"
        record = JournalEntryRead(
            entry_id=entry_id,
            content=entry.content,
            emotion=entry.emotion,
            tags=entry.tags,
            created_at=datetime.utcnow(),
            attachments=entry.attachments,
        )
        self._entries[entry_id] = record
        return record


repository = JournalRepository()
vector_store = VectorStore()
rag_engine = RagEngine(vector_store)
integration_manager = IntegrationManager()


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Simple health check endpoint."""

    return {"status": "ok"}


@app.get("/journal", response_model=List[JournalEntryRead])
def list_journal_entries() -> List[JournalEntryRead]:
    """Return the most recent journal entries in chronological order."""

    return repository.list_entries()


@app.post("/journal", response_model=JournalEntryRead, status_code=201)
def create_journal_entry(
    payload: JournalEntryCreate,
    store: VectorStore = Depends(lambda: vector_store),
) -> JournalEntryRead:
    """Persist a journal entry and index it inside the vector store.

    The vector store is currently an in-memory approximation. It exposes the
    same interface that future managed services (Pinecone, Weaviate, etc.) can
    implement, keeping the API layer stable while integrations evolve.
    """

    record = repository.add(payload)
    store.index(record)
    return record


@app.get("/journal/{entry_id}", response_model=JournalEntryRead)
def read_journal_entry(entry_id: str) -> JournalEntryRead:
    """Retrieve a single journal entry by identifier."""

    return repository.get(entry_id)


@app.get("/journal/search", response_model=List[JournalEntryRead])
def search_journal_entries(query: str, limit: Optional[int] = 5) -> List[JournalEntryRead]:
    """Perform similarity search over journal entries.

    The rag engine uses the vector store and can incorporate integrations later
    on (calendar events, Notion pages, etc.).
    """

    results = rag_engine.search(query, limit=limit)
    return [repository.get(entry_id) for entry_id in results]


@app.get("/integrations/status")
def integration_status() -> Dict[str, Dict[str, str]]:
    """Expose readiness status for third-party integrations."""

    return integration_manager.status_report()


@app.get("/calendar/next")
def upcoming_events() -> Dict[str, List[Dict[str, str]]]:
    """Provide stubbed upcoming calendar events sourced from integrations."""

    return {"events": integration_manager.calendar.next_events()}


@app.get("/notion/dashboards")
def notion_dashboards() -> Dict[str, List[Dict[str, str]]]:
    """Expose placeholder Notion dashboard metadata."""

    return {"dashboards": integration_manager.notion.available_dashboards()}


@app.get("/history/summary")
def history_summary() -> Dict[str, str]:
    """Summaries of historical journaling sessions generated via RAG."""

    summary = rag_engine.summarize(repository.list_entries())
    return {"summary": summary}


@app.get("/emotions", response_model=List[str])
def available_emotions() -> List[str]:
    """Expose the supported emotion labels for the frontend."""

    return [emotion.value for emotion in EmotionLabel]


__all__ = ["app"]
