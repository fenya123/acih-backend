"""Schemas for HTTP errors."""

from __future__ import annotations

from pydantic import BaseModel


class HTTPError(BaseModel):
    """Base schema for errors."""

    description: str
    detail: str


class NotAuthenticatedResponse(HTTPError):
    """Schema for 401 UNAUTHORIZED response."""


class NotFoundResponse(HTTPError):
    """Schema for 404 NOT FOUND error."""

    resource: str


class NotAllowedResponse(HTTPError):
    """Schema for 403 FORBIDDEN error."""

    action: str


class TooLargeResponse(HTTPError):
    """Schema for 413 ENTITY TOO LARGE response."""


class UnsupportedTypeResponse(HTTPError):
    """Schema for 415 UNSUPPORTED MEDIA TYPE response."""
