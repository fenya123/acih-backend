"""Routes for account package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Body, status

from src.account.schemas import AccountWithProfile, NewAccount


router = APIRouter(tags=["account"])


@router.post(
    "/accounts",
    response_model=AccountWithProfile,
    status_code=status.HTTP_201_CREATED,
)
def create_account(new_account: Annotated[NewAccount, Body()]) -> None:  # noqa: ARG001
    """Create account endpoint."""
