"""Package for auth models."""

from __future__ import annotations

import typing
import uuid
from typing import Self

from sqlalchemy import delete, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import Session as DBSession
from sqlalchemy.types import UUID

from src.shared.database import Base
from src.shared.exceptions import NotFoundException


class Session(Base):
    """ORM model for 'session' table."""

    __tablename__ = "session"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)  # noqa: A003

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False, unique=False)

    account: Mapped["Account"] = relationship("Account", back_populates="sessions")  # type: ignore[name-defined]  # noqa: F821,UP037,E501

    @classmethod
    def new_object(cls: type[Session], db: DBSession, account_id: int) -> Session:
        """Create session object."""
        session = Session(account_id=account_id)
        db.add(session)
        db.flush()
        return session

    @classmethod
    def get(cls: type[Session], db: DBSession, session_id: uuid.UUID) -> Session:
        """Get session object."""
        query = select(Session).where(Session.id == session_id)
        row = db.execute(query).one_or_none()
        if row is None:  # pragma: no cover
            msg = "Session not found."
            raise NotFoundException(msg)
        return typing.cast(Session, row.Session)

    def remove(self: Self, db: DBSession) -> None:
        """Remove session."""
        query = delete(Session).where(Session.id == self.id)
        db.execute(query)
