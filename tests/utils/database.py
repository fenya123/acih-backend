"""Database utilities for tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import text


if TYPE_CHECKING:
    from sqlalchemy.orm import scoped_session, Session


def set_autoincrement_counters(session: scoped_session[Session]) -> None:
    """Restart auto-increment counters on a value of 10000."""
    sequences = session.execute(text("SELECT sequencename FROM pg_sequences;")).fetchall()
    for seq in sequences:
        session.execute(text(f"ALTER SEQUENCE {seq[0]} RESTART WITH 10000;"))
