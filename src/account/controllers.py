"""Controllers for account package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.account.models import Account
from src.account.schemas import Account as AccountSchema
from src.account.schemas import AccountWithProfile
from src.profile.schemas import Profile as ProfileSchema
from src.shared.exceptions import NotFoundException


if TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from src.account.schemas import NewAccount


def create_account(new_account: NewAccount, db: Session) -> AccountWithProfile:
    """Create account."""
    new_account_instance = Account.create(
        db=db,
        email=new_account.email,
        username=new_account.username,
        password=new_account.password,
    )

    return AccountWithProfile(
        account=AccountSchema.model_validate(new_account_instance, from_attributes=True),
        profile=ProfileSchema.model_validate(new_account_instance.profile, from_attributes=True),
    )


def check_account_email(db: Session, email: str) -> bool:
    """Check whether account with a specified e-mail exists or not."""
    try:
        account = Account.get_by_email(db, email)
    except NotFoundException:
        return True
    return False
