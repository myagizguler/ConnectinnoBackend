# api

API layer: versioned routes and dependencies.

## Structure

```
api/
├── v1/
│   ├── router.py   # Aggregates all v1 routers
│   ├── items.py    # Example items CRUD
│   └── README.md
└── README.md
```

## Versioning

- All public routes live under **v1** (`/api/v1/...`).
- New versions (e.g. `v2/`) can be added as new packages; mount in `main.py` with a different prefix (e.g. `/api/v2`).

## Adding a New Route Module

1. Create a file under `api/v1/`, e.g. `users.py`, with an `APIRouter()`.
2. In `api/v1/router.py`, import the router and include it:

   ```python
   from app.api.v1 import items, users
   api_router.include_router(users.router, prefix="/users", tags=["users"])
   ```

Use `app.core.firebase.get_db()` (or a `Depends()` wrapper) inside route handlers to access Firebase.
