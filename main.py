"""Cloud Run entrypoint module.

Google Cloud Run (source deploy) by default looks for ``main:app``.
This file simply re-exports the FastAPI application defined in
``app/main.py`` so that ``gunicorn main:app`` works correctly.
"""

from app.main import app  # noqa: F401

