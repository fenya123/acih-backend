"""Global fixtures/settings/hooks etc."""

from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import UUID

import jwt
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.account.enums import Algorithm
from src.account.models import Account, PasswordHash
from src.app import app
from src.auth.models import Session
from src.auth.schemas import Algorithm as AuthAlgorithm
from src.config import config
from src.entity.models import Entity
from src.files.enums import Extension, MimeType
from src.files.models import File
from src.following.models import Following
from src.profile.models import Profile
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
def db_with_one_account(db_empty):
    """Create database with one account (and password hash)."""
    session = db_empty
    test_account = Account(
        id=1,
        email="test@gmail.com",
    )
    session.add(test_account)

    salt = "e570d2d0-0515-49ee-9f08-68f34026028c"
    salted_password = "testpassword" + salt
    hash_object = hashlib.new(Algorithm.SHA256.value)
    hash_object.update(salted_password.encode("ascii"))

    test_password_hash = PasswordHash(
        account_id=1,
        algorithm=Algorithm.SHA256,
        salt=UUID(salt),
        value=hash_object.hexdigest(),
    )
    session.add(test_password_hash)

    profile = Profile(
        account_id=1,
        username="test",
    )
    session.add(profile)
    session.commit()
    return session


@pytest.fixture
def db_with_one_account_and_two_files(db_with_one_account_one_session):
    """Create database with one account and two unrelated files."""
    session = db_with_one_account_one_session
    session.add_all([
        File(
            id=1,
            extension=Extension.JPG,
            filename="testjpg.jpg",
            mime_type=MimeType.IMAGE_JPEG,
            size=15,
        ),
        File(
            id=2,
            extension=Extension.PNG,
            filename="testpng.png",
            mime_type=MimeType.IMAGE_PNG,
            size=15,
        ),
    ])
    session.commit()
    return session


@pytest.fixture
def db_with_two_accounts_one_session(db_with_one_account_one_session):
    """Create database with two accounts."""
    session = db_with_one_account_one_session
    test_account = Account(
        id=2,
        email="test02@gmail.com",
    )
    session.add(test_account)

    salt = "7d360089-5dcd-4216-9e92-bc4d836a443b"
    salted_password = "testpassword02" + salt
    hash_object = hashlib.new(Algorithm.SHA256.value)
    hash_object.update(salted_password.encode("ascii"))

    test_password_hash = PasswordHash(
        account_id=2,
        algorithm=Algorithm.SHA256,
        salt=UUID(salt),
        value=hash_object.hexdigest(),
    )
    session.add(test_password_hash)

    profile = Profile(
        account_id=2,
        username="test02",
    )
    session.add(profile)
    session.commit()
    return session


@pytest.fixture
def db_with_two_accounts_one_session_one_following(db_with_two_accounts_one_session):
    """Create database with two accounts, with the one authorized following the other."""
    session = db_with_two_accounts_one_session
    test_following = Following(
        id=1,
        follower_id=1,
        followee_id=2,
    )
    session.add(test_following)
    session.commit()
    return session


@pytest.fixture
def db_with_several_following_relationsips(db_empty):
    """Several accounts with different following relationships."""
    session = db_empty
    session.add_all([
        Account(id=1, email="test1@gmail.com"),
        Account(id=2, email="test2@gmail.com"),
        Account(id=3, email="test3@gmail.com"),
    ])
    session.flush()

    salt = "e570d2d0-0515-49ee-9f08-68f34026028c"
    salted_password = "testpassword" + salt
    hash_object = hashlib.new(Algorithm.SHA256.value)
    hash_object.update(salted_password.encode("ascii"))
    session.add_all([
        PasswordHash(account_id=1, algorithm=Algorithm.SHA256, salt=UUID(salt), value=hash_object.hexdigest()),
        PasswordHash(account_id=2, algorithm=Algorithm.SHA256, salt=UUID(salt), value=hash_object.hexdigest()),
        PasswordHash(account_id=3, algorithm=Algorithm.SHA256, salt=UUID(salt), value=hash_object.hexdigest()),
    ])
    session.flush()

    session.add_all([
        Profile(account_id=1, username="test1"),
        Profile(account_id=2, username="test2"),
        Profile(account_id=3, username="test3"),
    ])
    session.flush()
    session.commit()

    session.add_all([
        Following(id=1, follower_id=1, followee_id=2),
        Following(id=2, follower_id=1, followee_id=3),

        Following(id=3, follower_id=3, followee_id=1),
        Following(id=4, follower_id=3, followee_id=2),
    ])
    session.flush()

    test_session = Session(
        id=UUID("441d78c0-c031-4fa6-9f2a-78200da5c0fe"),
        account_id=1,
    )
    session.add(test_session)
    session.flush()
    return session


@pytest.fixture
def db_with_one_account_one_session(db_with_one_account):
    """Create database with one account (and password hash) with a session."""
    session = db_with_one_account
    test_session = Session(
        id=UUID("441d78c0-c031-4fa6-9f2a-78200da5c0fe"),
        account_id=1,
    )
    session.add(test_session)
    session.commit()
    return session


@pytest.fixture
def db_with_one_account_one_other_session(db_with_one_account):
    """Add a different session to the same account."""
    session = db_with_one_account
    test_session = Session(
        id=UUID("41cd3cfe-6b14-48a1-8117-f8ba3a7a09af"),
        account_id=1,
    )
    session.add(test_session)
    session.commit()
    return session


@pytest.fixture
def token_for_testing():
    """JWT token shortcut."""
    payload = {
        "account_id": 1,
        "session_id": "441d78c0-c031-4fa6-9f2a-78200da5c0fe",
    }
    return jwt.encode(payload, config.SECRET_KEY, AuthAlgorithm.HS256.value)


@pytest.fixture
def token_with_false_secret_key():
    """Invalid signature token."""
    payload = {
        "account_id": 1,
        "session_id": "441d78c0-c031-4fa6-9f2a-78200da5c0fe",
    }
    return jwt.encode(payload, "false_secret", AuthAlgorithm.HS256.value)


@pytest.fixture
def db_with_one_entity(db_empty):
    """Create database with one Entity."""
    session = db_empty
    new_entity = Entity(id=1)
    session.add(new_entity)
    session.commit()
    return session


@pytest.fixture
def db_with_one_file(db_empty):
    """Create db with one 'image' file."""
    session = db_empty
    file = File(
        extension=Extension.JPG,
        filename="testjpg.jpg",
        mime_type=MimeType.IMAGE_JPEG,
        size=15,
    )
    session.add(file)
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


@pytest.fixture
def storage_with_one_object(storage_empty, tmp_path):
    """Storage with one bucket with one object."""
    filepath = Path(tmp_path) / "testobject.txt"
    filepath.write_bytes(b"Mockbytesobject")
    storage_empty.fput_object(
        bucket_name=storage_empty.BUCKETS[0],
        object_name="10000",
        file_path=filepath,
    )
    return storage_empty
