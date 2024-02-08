"""Package for auth models."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session as DBSession
from sqlalchemy.types import UUID

from src.shared.database import Base


class Session(Base):  # pylint: disable=too-few-public-methods
    """ORM model for 'session' table."""

    __tablename__ = "session"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)  # noqa: A003

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False, unique=False)

    @classmethod
    def new_object(cls: type[Session], db: DBSession, account_id: int) -> Session:
        """Create session object."""
        session = Session(account_id=account_id)
        db.add(session)
        db.flush()
        return session
