"""Routes for health package."""

from __future__ import annotations

from fastapi import APIRouter, status

from src.health import enums, schemas


router = APIRouter(tags=["service"])


@router.get(
    "/health",
    responses={
        status.HTTP_200_OK: {"description": "Backend application works fine."},
    },
    status_code=status.HTTP_200_OK,
    summary="Check health.",
)
async def get_health() -> schemas.Health:
    """Check back-end health."""
    return schemas.Health(status=enums.HealthStatus.OK)
