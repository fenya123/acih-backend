"""Pydantic schemas for SQLAlchemy models."""

from __future__ import annotations

from pydantic import BaseModel


class EntitySchema(BaseModel):
    """Pydantic schema for Entity model."""

    id: int  # noqa: A003

    class Config:
        """Configuration for Pydantic schema."""

        orm_mode = True


class EntitiesSchema(BaseModel):
    """Pydantic schema for multiple entities."""

    entities: list[EntitySchema]
