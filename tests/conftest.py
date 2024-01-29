"""Global fixtures/settings/hooks etc."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.app import app
from src.config import config
from src.entity.models import Entity
from src.shared.database import get_db
from src.shared.storage import Minio
from tests.utils.database import set_autoincrement_counters


@pytest.fixture
def db_empty():
    """Create clean database with built-in cleanup."""
    engine = create_engine(config.POSTGRES_CONNECTION_URI)
    connection = engine.connect()
    transaction = connection.begin()
    session = scoped_session(sessionmaker(bind=connection))
    set_autoincrement_counters(session)
    yield session
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_empty):
    """FastAPI test client."""
    def override_get_db():
        yield db_empty
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def db_with_one_entity(db_empty):
    """Create database with one Entity."""
    session = db_empty
    new_entity = Entity(id=1)
    session.add(new_entity)
    session.commit()
    return session


@pytest.fixture
def storage_empty():
    """Return Minio client and clean the storage before testing."""
    minio_client = Minio(
        f"{config.MINIO_HOST}:{config.MINIO_PORT}",
        access_key=config.MINIO_ACCESS_KEY,
        secret_key=config.MINIO_SECRET_KEY,
        secure=False,
    )
    buckets = minio_client.list_buckets()

    for bucket in buckets:
        objects = minio_client.list_objects(bucket.name, recursive=True)
        for obj in objects:
            minio_client.remove_object(bucket.name, obj.object_name)

    return minio_client
