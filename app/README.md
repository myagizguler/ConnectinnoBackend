# app

Main application package for the Connectinno backend.

## Contents

| Path | Purpose |
|------|--------|
| `main.py` | FastAPI app instance, lifespan (Firebase init/close), router mounting |
| `config.py` | Pydantic Settings: loads `.env`, exposes `settings` |
| `api/` | API versioning and route modules |
| `core/` | Firebase client, shared dependencies |
| `models/` | Pydantic request/response schemas |
| `services/` | Business logic and Firebase operations |
| `utils/` | Shared helpers |

## Entry Point

Run with:

```bash
uvicorn app.main:app --reload
```

The app initializes Firebase on startup (see `main.py` lifespan) and exposes `/api/v1/*` and `/health`.
