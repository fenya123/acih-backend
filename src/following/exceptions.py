"""Files package exceptions."""

from __future__ import annotations

from fastapi import status

from src.shared.exceptions import ForbiddenException, NotFoundException


class NotOwnedAccountFollowerException(ForbiddenException):
    """Creating following where follower isn't the owned account."""

    action: str = "Create following"

    description = "Requested action not allowed."
    detail = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class FollowingAlreadyExistsException(ForbiddenException):
    """Following already exists exception."""

    action: str = "Create existing following"

    description = "Requested action not allowed."
    detail = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class NotOwnedAccountFolloweeException(ForbiddenException):
    """Removing following where followee isn't the owned account."""

    action: str = "Remove following"

    description = "Requested action not allowed."
    detail = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class FollowingNotFoundException(NotFoundException):
    """Following does not exist exception."""

    resource: str = "Following"

    description = "Requested resource not found."
    detail = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND
