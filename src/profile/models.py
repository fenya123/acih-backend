"""Package for profile models."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from src.shared.database import Base


class Profile(Base):  # pylint: disable=too-few-public-methods
    """ORM model of 'profile' table."""

    __tablename__ = "profile"

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), primary_key=True)

    avatar_id: Mapped[int | None] = mapped_column(Integer, nullable=True, unique=True)
    background_id: Mapped[int | None] = mapped_column(Integer, nullable=True, unique=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    info: Mapped[str | None] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    account: Mapped["Account"] = relationship(back_populates="profile")  # type: ignore[name-defined]  # noqa: F821,UP037,E501

    @classmethod
    def new_object(cls: type[Profile], db: Session, username: str, account_id: int) -> Profile:
        """Create new Profile object."""
        new_profile = Profile(username=username, account_id=account_id)
        db.add(new_profile)
        db.flush()
        return new_profile
