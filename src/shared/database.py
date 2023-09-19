"""Module for database utilities."""

from __future__ import annotations

from typing import Annotated, TYPE_CHECKING

from fastapi import Depends
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase, scoped_session, Session, sessionmaker


if TYPE_CHECKING:
    from collections.abc import Iterator


connection_uri = URL.create(
    "postgresql",
    username="pu",
    password="pp",  # noqa: S106
    host="localhost",
    port=5432,
    database="postgres",
)

# will allow us to connect to PostgreSQL database
engine = create_engine(connection_uri)

# will allow us to send SQL queries to database associated with engine
session = scoped_session(sessionmaker(bind=engine))


# will allow us to map relation tables from PostgreSQL to python classes
# each model must inherit this Base class
class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Subclass this to map Python objects to SQL data."""


# will allow us to create a separate database connection for each request
# and close it when the request is finished
def get_db() -> Iterator[scoped_session[Session]]:
    """Create session for a request then close it when request is done."""
    try:
        yield session
    finally:
        session.close()


# used by FastAPI routes to inject database session dependency
Db = Annotated[Session, Depends(get_db)]
