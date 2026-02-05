"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import __version__
from app.config import settings
from app.core.firebase import init_firebase, close_firebase
from app.api.auth import router as auth_router
from app.api.v1 import notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    init_firebase()
    yield
    close_firebase()


app = FastAPI(
    title=settings.app_name,
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth_router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": __version__}
