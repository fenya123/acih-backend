"""Package for profile models."""

from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, Session

from src.shared.database import Base


class Following(Base):  # pylint: disable=too-few-public-methods
    """ORM model of 'following' table."""

    __tablename__ = "following"

    id: Mapped[int] = mapped_column(primary_key=True)  # noqa: A003

    follower_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False, unique=False)
    followee_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False, unique=False)

    __table_args__ = (
        CheckConstraint("follower_id != followee_id", name="check_following_self"),
        UniqueConstraint("follower_id", "followee_id", name="unique_following"),
    )

    @classmethod
    def new_object(cls: type[Following], db: Session, followee_id: int, follower_id: int) -> Following:
        """Create following object."""
        following_object = Following(
            follower_id=follower_id,
            followee_id=followee_id,
        )
        db.add(following_object)
        db.flush()
        return following_object
