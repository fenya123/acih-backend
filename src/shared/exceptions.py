"""Module for exception utilities."""

from __future__ import annotations

from fastapi import status


class HTTPException(Exception):
    """Default exception class."""

    description = "Unexpected error had occured."
    detail = "Please contact backend maintenance team."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class UnauthorizedException(HTTPException):
    """Exception for 401 UNAUTHORIZED error."""

    description = "Request initiator is not authenticated."
    detail = "Your credentials or tokens are invalid or missing."
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenException(HTTPException):
    """Exception for 403 FORBIDDEN error."""

    action: str

    description = "Requested action not allowed."
    detail = "Provided tokens or credentials don't grant you enough access rights."
    status_code = status.HTTP_403_FORBIDDEN


class NotFoundException(HTTPException):
    """Exception for 404 NOT FOUND error."""

    resource: str

    description = "Requested resource not found."
    detail = "Requested resource doesn't exist or has been deleted."
    status_code = status.HTTP_404_NOT_FOUND


class EntityTooLargeException(HTTPException):
    """Exception for 413 REQUEST ENTITY TOO LARGE error."""

    description = "Request payload is too large."
    detail = "Request payload is too large, and cannot be handled."
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class UnsupportedTypeException(HTTPException):
    """Exception for 415 UNSUPPORTED MEDIA TYPE error."""

    description = "Request payload type is not supported."
    detail = "Request payload type is not supported, and cannot be handled."
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
