"""Pydantic schemas for auth feature."""

from __future__ import annotations

from typing import Self
from uuid import UUID

import jwt
from pydantic import BaseModel

from src.auth.enums import Algorithm
from src.config import config


class Credentials(BaseModel):
    """Credentials schema."""

    email: str
    password: str


class Session(BaseModel):
    """Session schema."""

    id: UUID  # noqa: A003

    account_id: int


class SessionWithToken(BaseModel):
    """Session with token schema."""

    session: Session
    token: str


class TokenPayload(BaseModel):
    """Token payload schema."""

    session_id: UUID
    account_id: int

    @property
    def token(self: Self) -> str:
        """Encode data into JWT token."""
        payload_data = {
            "account_id": self.account_id,
            "session_id": str(self.session_id),
        }
        return jwt.encode(payload_data, config.SECRET_KEY, Algorithm.HS256.value)
