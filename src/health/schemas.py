"""Pydantic schemas for health feature."""

from __future__ import annotations

from pydantic import BaseModel, Field

from src.health.enums import HealthStatus


class Health(BaseModel):
    """Schema for a health status."""

    status: HealthStatus = Field(..., examples=[HealthStatus.OK])
