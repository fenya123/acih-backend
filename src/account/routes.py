"""Routes for account package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Path, status

from src.account import controllers
from src.account.schemas import AccountWithProfile, NewAccount
from src.shared.database import Db


router = APIRouter(tags=["account"])


@router.post(
    "/accounts",
    response_model=AccountWithProfile,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    db: Db,
    new_account: Annotated[NewAccount, Body()],
) -> AccountWithProfile:
    """Create account endpoint."""
    return controllers.create_account(new_account=new_account, db=db)


@router.get(
    "/accounts/{email}",
    status_code=status.HTTP_200_OK,
)
def check_account_email(
    db: Db,
    email: Annotated[str, Path()],
) -> bool:
    """Check whether account with a specified e-mail exists or not."""
    return controllers.check_account_email(db, email)
