"""Project wide Swagger utilities."""

from __future__ import annotations

from fastapi import status

from src.shared.exceptions import (
    EntityTooLargeException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    UnsupportedTypeException,
)
from src.shared.schemas import (
    NotAllowedResponse,
    NotAuthenticatedResponse,
    NotFoundResponse,
    TooLargeResponse,
    UnsupportedTypeResponse,
)


responses = {  # pylint: disable=consider-using-namedtuple-or-dataclass
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Provided tokens or credentials are invalid or missing.",
        "model": NotAuthenticatedResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": UnauthorizedException.description,
                    "details": UnauthorizedException.detail,
                },
            },
        },
    },

    status.HTTP_403_FORBIDDEN: {
        "description": "Provided tokens or credentials don't grant you enough access rights.",
        "model": NotAllowedResponse,
        "content": {
            "application/json": {
                "example": {
                    "action": "<requested action description will be here>",
                    "description": ForbiddenException.description,
                    "details": ForbiddenException.detail,
                },
            },
        },
    },

    status.HTTP_404_NOT_FOUND: {
        "description": "Requested resource doesn't exist.",
        "model": NotFoundResponse,
        "content": {
            "application/json": {
                "example": {
                    "resource": "<requested resource description will be here>",
                    "description": NotFoundException.description,
                    "details": NotFoundException.detail,
                },
            },
        },
    },

    status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {
        "description": "Request payload exceeds allowed size.",
        "model": TooLargeResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": EntityTooLargeException.description,
                    "details": EntityTooLargeException.detail,
                },
            },
        },
    },

    status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {
        "description": "Request payload's media type is not supported.",
        "model": UnsupportedTypeResponse,
        "content": {
            "application/json": {
                "example": {
                    "description": UnsupportedTypeException.description,
                    "details": UnsupportedTypeException.detail,
                },
            },
        },
    },
}
