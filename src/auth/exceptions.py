"""Auth package exceptions."""

from __future__ import annotations

from fastapi import status

from src.shared.exceptions import ForbiddenException, NotFoundException, UnauthorizedException


class SessionRemovalException(ForbiddenException):
    """Remove session exception."""

    action: str = "Remove session"

    description = "Requested action not allowed."
    detail = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class InvalidTokenException(UnauthorizedException):
    """Invalid token exception."""

    description = "Request initiator is not authenticated."
    detail = "Your credentials or tokens are invalid or missing."
    status_code = status.HTTP_401_UNAUTHORIZED


class SessionNotFoundException(NotFoundException):
    """Session not found exception."""

    resource: str = "Session"

    description = "Requested resource not found."
    detail = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND
