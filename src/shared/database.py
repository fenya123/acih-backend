"""Module for database utilities."""

from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, Session, sessionmaker

from src.config import config


if TYPE_CHECKING:
    from collections.abc import Iterator


# will allow us to connect to PostgreSQL database
engine = create_engine(config.POSTGRES_CONNECTION_URI)

# will allow us to send SQL queries to database associated with engine
session = scoped_session(sessionmaker(bind=engine))


# will allow us to map relation tables from PostgreSQL to python classes
# each model must inherit this Base class
class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Subclass this to map Python objects to SQL data."""


# will allow us to create a separate database connection for each request
# and close it when the request is finished
def get_db() -> Iterator[scoped_session[Session]]:  # pragma: no cover
    """Create session for a request then close it when request is done."""
    try:  # pylint: disable=too-many-try-statements
        yield session
        session.commit()
    except Exception:  # noqa: BLE001
        session.rollback()
    finally:
        session.close()


# used by FastAPI routes to inject database session dependency
Db = Annotated[Session, Depends(get_db)]
