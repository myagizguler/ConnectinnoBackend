# models

Pydantic models for request and response bodies and shared DTOs.

## Note app

### note.py

| Model | Purpose |
|-------|---------|
| **NoteCreate** | Create payload: `title` (required), `content` (default `""`), `tags` (list, max 20). |
| **NoteUpdate** | Partial update: `title`, `content`, `tags` (all optional). |
| **NoteResponse** | API response: `id`, `user_id`, `title`, `content`, `tags`, `created_at`, `updated_at`. |

Used by `api/v1/notes.py` for all note endpoints. `NoteResponse` coerces Firestore timestamp-like values to `datetime`.

## Usage

- **Request bodies**: Use the model as a route parameter, e.g. `async def create_note(body: NoteCreate):`
- **Response**: Use `response_model=NoteResponse` for consistent JSON and OpenAPI.
- Prefer one module per domain and re-export from `models/__init__.py` if desired.
