"""Package for profile models."""

from __future__ import annotations

import typing
from typing import Self

from sqlalchemy import ForeignKey, select, String, update
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from src.profile.schemas import ProfileData
from src.shared.database import Base


class Profile(Base):
    """ORM model of 'profile' table."""

    __tablename__ = "profile"

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), primary_key=True)

    avatar_id: Mapped[int | None] = mapped_column(ForeignKey("file.id"), nullable=True, unique=True)
    background_id: Mapped[int | None] = mapped_column(ForeignKey("file.id"), nullable=True, unique=True)
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

    @classmethod
    def get_multiple(cls: type[Profile], db: Session, account_ids: list[int]) -> list[Profile]:
        """Get multiple profiles by primary key."""
        query = select(Profile).where(Profile.account_id.in_(account_ids))
        rows = db.execute(query).all()
        return [typing.cast(Profile, row.Profile) for row in rows]

    @classmethod
    def exists(cls: type[Profile], db: Session, username: str) -> bool:
        """Check whether profile with a specified username exists or not."""
        query = select(Profile).where(Profile.username == username)
        row = db.execute(query).one_or_none()

        return row is not None

    def update(self: Self, profile_data: ProfileData, db: Session) -> None:
        """Update profile's database object."""
        query = (
            update(Profile)
            .where(Profile.account_id == self.account_id)
            .values(
                avatar_id=profile_data.avatar_id,
                background_id=profile_data.background_id,
                description=profile_data.description,
                info=profile_data.info,
                username=profile_data.username,
            )
        )
        db.execute(query)
