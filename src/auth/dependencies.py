"""Fastapi dependencies for auth feature."""

from __future__ import annotations

from fastapi.security import HTTPBearer


get_token = HTTPBearer()
