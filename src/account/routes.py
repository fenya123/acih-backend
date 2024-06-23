"""Routes for account package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, Query, status

from src.account import controllers
from src.account.schemas import AccountWithProfile, ExistenceCheck, NewAccount
from src.shared.database import Db


router = APIRouter(tags=["account"])


@router.post(
    "/accounts",
    responses={
        status.HTTP_201_CREATED: {"description": "New account and profile are created."},
    },
    response_model=AccountWithProfile,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    db: Db,
    new_account: Annotated[NewAccount, Body()],
) -> AccountWithProfile:
    """Sign up to create account and profile."""
    return controllers.create_account(new_account=new_account, db=db)


@router.get(
    "/accounts/exists",
    responses={
        status.HTTP_200_OK: {"description": "True means account exists, False otherwise."},
    },
    status_code=status.HTTP_200_OK,
)
def check_account_exists(
    db: Db,
    email: Annotated[str, Query(example="test@gmail.com")],
) -> ExistenceCheck:
    """Check whether account with a specified e-mail exists or not."""
    return controllers.check_account_exists(db, email)


@router.get(
    "/profiles/exists",
    responses={
        status.HTTP_200_OK: {"description": "True means profile exists, False otherwise."},
    },
)
def check_profile_exists(
    db: Db,
    username: Annotated[str, Query(example="bob1997")],
) -> ExistenceCheck:
    """Check whether profile with a specified username exists or not."""
    return controllers.check_profile_exists(db, username)
