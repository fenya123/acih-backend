"""Pydantic schemas for auth feature."""

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class Credentials(BaseModel):
    """Credentials schema."""

    email: str
    password: str


class Session(BaseModel):
    """Session schema."""

    id: UUID  # noqa: A003

    account_id: int
    token: str
