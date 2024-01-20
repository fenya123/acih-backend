"""Pydantic schemas for account feature."""

from __future__ import annotations

from pydantic import BaseModel, Field

from src.profile.schemas import Profile


class NewAccount(BaseModel):
    """Schema for an account to be created."""

    email: str = Field(min_length=5, max_length=200, pattern=r".+@.+\..+", examples=["test_eMaiL_2024@gmail.com"])
    password: str = Field(min_length=8, max_length=500, examples=["Placeholder!Password@For-Swagger?UI"])
    username: str = Field(min_length=1, max_length=30, pattern=r"[a-z][a-z0-9_]*")


class Account(BaseModel):
    """Account schema."""

    id: int  # noqa: A003

    email: str = Field(min_length=5, max_length=200, pattern=r".+@.+\..+", examples=["test_eMaiL_2024@gmail.com"])


class Accounts(BaseModel):
    """Accounts (plural) schema."""

    accounts: list[Account]


class AccountWithProfile(BaseModel):
    """Schema for Account and Profile."""

    account: Account
    profile: Profile
