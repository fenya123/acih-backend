"""Controllers for search package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.profile.models import Profile
from src.profile.schemas import Profiles


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def search_profiles(
    db: Session,
    profile_username: str,
    limit: int,
    offset: int,
) -> Profiles:
    """Get profiles search result endpoint."""
    profiles = Profile.search_profiles(
        db=db,
        profile_username=profile_username,
        limit=limit,
        offset=offset,
    )

    return Profiles(profiles=profiles)
