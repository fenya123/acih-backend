"""Profile package exceptions."""

from __future__ import annotations

from fastapi import status

from src.shared.exceptions import ForbiddenException


class UpdateNotOwnedProfileException(ForbiddenException):
    """Update profile not owned by the user."""

    action: str = "Update profile"

    description = "Updating not owned profiles is not allowed."
    detail = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN
