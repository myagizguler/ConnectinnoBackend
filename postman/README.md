# Postman – Connectinno Notes API

## Import

1. Open Postman → **Import** → **Upload Files**
2. Select `Connectinno-Notes-API.postman_collection.json`

## Variables

Set these in the collection (or in an environment):

| Variable | Example | Description |
|----------|---------|-------------|
| `base_url` | `http://localhost:8000` | API base URL (register, login, notes) |
| `firebase_id_token` | `eyJhbGc...` | **From Register or Login response** – copy `id_token` here |
| `note_id` | (empty at start) | Set after **Create note**; used by **Update note** and **Delete note** |

## 401 Unauthorized?

1. Open folder **Auth** in the collection.
2. Run **1. Register** (or **2. Login** if you already have an account). Use the same `base_url` as your backend.
3. From the response, copy the **id_token** value.
4. In the collection, set variable **firebase_id_token** = that id_token.
5. Then run **List notes** or **Create note** – they will use this token.

## Requests

| Name | Method | URL | Body |
|------|--------|-----|------|
| Register | POST | `/register` | JSON: `email`, `password`, `display_name?` |
| Login | POST | `/login` | JSON: `email`, `password` |
| List notes | GET | `/notes` | — |
| Create note | POST | `/notes` | JSON: `title`, `content`, `tags` |
| Update note | PUT | `/notes/{{note_id}}` | JSON: optional `title`, `content`, `tags` |
| Delete note | DELETE | `/notes/{{note_id}}` | — |

## Getting the id_token

Call **POST /register** (new user) or **POST /login** (existing user) on this API. The response includes **id_token** – copy it into the collection variable **firebase_id_token**.

## Example JSON bodies

### POST /notes (Create note)

```json
{
  "title": "My first note",
  "content": "This is the note content.",
  "tags": ["work", "ideas"]
}
```

- `title`: required, 1–256 chars  
- `content`: optional, default `""`, max 50_000 chars  
- `tags`: optional, default `[]`, max 20 items  

### PUT /notes/{id} (Update note – partial)

```json
{
  "title": "Updated title"
}
```

or

```json
{
  "content": "Only content updated.",
  "tags": ["new-tag"]
}
```

All fields are optional; send only the fields you want to change.
