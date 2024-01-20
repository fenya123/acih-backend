"""Routes for account package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, status

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
