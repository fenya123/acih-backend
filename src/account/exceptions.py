"""Account package exceptions."""

from __future__ import annotations

from fastapi import status

from src.shared.exceptions import NotFoundException


class AccountNotFoundException(NotFoundException):
    """Account not found exception."""

    resource: str = "Account"

    description = "Requested resource not found."
    detail = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND
