"""Pydantic schemas for account feature."""

from __future__ import annotations

from pydantic import BaseModel

from src.profile.schemas import Profile


class NewAccount(BaseModel):
    """Schema for an account to be created."""

    email: str
    password: str
    username: str


class Account(BaseModel):
    """Account schema."""

    id: int  # noqa: A003

    email: str


class Accounts(BaseModel):
    """Accounts (plural) schema."""

    accounts: list[Account]


class AccountWithProfile(BaseModel):
    """Schema for Account and Profile."""

    account: Account
    profile: Profile
