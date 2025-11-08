# AI Aisant Emotional Companion

This repository provides an end-to-end prototype for an AI assisted journaling companion. It includes:

- **FastAPI backend** with journaling endpoints, Retrieval Augmented Generation (RAG) scaffolding, and placeholder integrations for Gmail Calendar and Notion.
- **Lightweight frontend** that renders expressive emotion faces while journaling, shows history, and mocks an assistant chat flow.
- **Vector store stub** so the API can expose similarity search without external dependencies.

The goal is to offer a deployment-ready starting point that can be extended with production integrations, managed vector databases, and full multimodal experiences.

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API exposes:

- `GET /health` – service heartbeat
- `POST /journal` – create a journal entry (persisted in memory & indexed)
- `GET /journal` – list entries
- `GET /journal/{entry_id}` – retrieve a specific entry
- `GET /journal/search?query=` – similarity search via the vector store stub
- `GET /history/summary` – RAG-style summary of all entries
- `GET /emotions` – enumeration of supported emotions for the UI
- `GET /integrations/status` – Gmail / Notion connectivity readiness report
- `GET /calendar/next` – sample calendar events sourced from the Gmail stub
- `GET /notion/dashboards` – placeholder Notion dashboards

Future integrations (Gmail OAuth, Notion databases, MCP tools, etc.) can replace the stubs in `backend/app/services` without touching the API surface.

### Frontend

The frontend is a static HTML page that calls the API running on `http://localhost:8000`.

```bash
cd frontend
python3 -m http.server 5173
```

Navigate to `http://localhost:5173` while the backend is running. The UI allows you to:

1. Select your current emotion and watch the companion face react.
2. Write journal entries and store them via the backend.
3. Review historical entries with context retrieved from the vector store.
4. Trigger a summary that demonstrates how the RAG pipeline will respond.
5. Interact with a placeholder chat companion to test the conversational layout.

### Roadmap

- Replace the in-memory vector store with a managed service (Pinecone, Weaviate, pgvector, etc.).
- Add Managed Collaboration Protocol (MCP) tooling for structured workflows.
- Connect to Gmail, Notion, and Google Calendar via OAuth with token storage.
- Expand to multimodal capture (video, audio) for vlog-style journaling.
- Generate graph visualisations of emotional journeys and context maps.
- Package the frontend + backend using Docker for single-command deployment.

## Project Structure

```
backend/
  app/
    main.py
    models.py
    services/
      integrations.py
      rag.py
      vector_store.py
  requirements.txt
frontend/
  index.html
```

This scaffold is intentionally lightweight so you can evolve it into a production-grade emotional companion with advanced AI workflows.
