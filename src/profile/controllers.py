"""Controllers for profile package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from src.account.models import Account
from src.profile.models import Profile as ProfileModel
from src.profile.schemas import Profile, Profiles


if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from src.auth.schemas import TokenPayload
    from src.profile.schemas import ProfileData


def update_profile(account_id: int, db: Session, profile_data: ProfileData, token: TokenPayload) -> Profile:
    """Update profile data."""
    if token.account_id != account_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No rights to perform that action")

    account = Account.get(account_id=account_id, db=db)
    account.profile.update(profile_data=profile_data, db=db)

    return Profile.model_validate(account.profile, from_attributes=True)


def get_profile(account_id: int, db: Session) -> Profile:
    """Get profile by id."""
    account = Account.get(account_id=account_id, db=db)

    return Profile.model_validate(account.profile, from_attributes=True)


def get_profiles(account_ids: list[int], db: Session) -> Profiles:
    """Get several profiles."""
    profiles = ProfileModel.get_multiple(db, account_ids)

    return Profiles.model_validate({"profiles": profiles}, from_attributes=True)
