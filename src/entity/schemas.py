"""Pydantic schemas for SQLAlchemy models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class EntitySchema(BaseModel):
    """Pydantic schema for Entity model."""

    id: int  # noqa: A003
    model_config = ConfigDict(from_attributes=True)


class EntitiesSchema(BaseModel):
    """Pydantic schema for multiple entities."""

    entities: list[EntitySchema]
