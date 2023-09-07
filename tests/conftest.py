"""Global fixtures/settings/hooks etc."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)
