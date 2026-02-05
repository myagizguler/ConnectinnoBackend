"""Pydantic models for auth (register, login)."""

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """Payload for POST /register."""

    email: str = Field(..., min_length=1, max_length=256)
    password: str = Field(..., min_length=6, max_length=128)
    display_name: str | None = Field(None, max_length=128)


class LoginRequest(BaseModel):
    """Payload for POST /login."""

    email: str = Field(..., min_length=1, max_length=256)
    password: str = Field(..., min_length=1, max_length=128)


class AuthResponse(BaseModel):
    """Response for register and login (id_token for Authorization header)."""

    id_token: str
    refresh_token: str
    uid: str
    email: str
    expires_in: int
