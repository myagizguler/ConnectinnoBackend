# api v1

Version 1 of the public API (note app).

## Routers

| Prefix | Module | Description |
|--------|--------|-------------|
| `/notes` | `notes.py` | CRUD for notes (Firestore) |

## Authentication

All note endpoints require **Firebase Auth**: send the Firebase ID token in the header:

```http
Authorization: Bearer <firebase_id_token>
```

The backend verifies the token and uses the **uid** as `user_id`; notes are stored and returned only for that user.

## Usage

- **List notes**: `GET /notes` – list user's notes
- **Create note**: `POST /notes` – body `{ "title": "...", "content": "...", "tags": [] }`
- **Update note**: `PUT /notes/{id}` – partial body
- **Delete note**: `DELETE /notes/{id}`

## Conventions

- One router per resource or domain. Register each in `router.py` with a prefix and tags for Swagger.
- Use Pydantic models from `app.models` for request/response bodies.
