"""Project wide Swagger utilities."""
from __future__ import annotations

from src.shared.enums import Enum


class Description(Enum):
    """HTTP status code descriptions for Swagger documentation."""

    HTTP_401 = "Provided tokens or credentials are invalid or missing."
    HTTP_403 = "Provided tokens or credentials don't grant you enough access rights."
    HTTP_404 = "Requested resource doesn't exist."
