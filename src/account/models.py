"""Package for account models."""

from __future__ import annotations

import hashlib
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from src.account.enums import Algorithm
from src.profile.models import Profile
from src.shared.database import Base


if TYPE_CHECKING:
    from typing import Self


class Account(Base):
    """ORM model for 'account' table."""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003

    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    profile: Mapped["Profile"] = relationship(uselist=False, back_populates="account")  # noqa: UP037

    @classmethod
    def create(
        cls: type[Account],
        db: Session,
        email: str,
        username: str,
        password: str,
    ) -> Account:
        """Create new account, profile and password hash, return account object."""
        new_account = Account.new_object(db, email)
        PasswordHash.new_object(db, password, new_account.id)
        Profile.new_object(db, username, new_account.id)
        return new_account

    @classmethod
    def new_object(cls: type[Account], db: Session, email: str) -> Account:
        """Create new Account object."""
        new_account = Account(email=email)
        db.add(new_account)
        db.flush()
        return new_account


class PasswordHash(Base):  # pylint: disable=too-few-public-methods
    """ORM model for the 'password_hash' table."""

    __tablename__ = "password_hash"

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), primary_key=True)

    algorithm: Mapped[Algorithm] = mapped_column(Enum(Algorithm, name="algorithm_enum"), nullable=False)
    salt: Mapped[str] = mapped_column(String(36), nullable=False)
    value: Mapped[str] = mapped_column(String(128), nullable=False)

    @classmethod
    def new_object(cls: type[PasswordHash], db: Session, password: str, account_id: int) -> PasswordHash:
        """Create new PasswordHash object."""
        new_password_hash = PasswordHash(account_id=account_id)
        new_password_hash._hash_password(password)  # noqa: SLF001
        db.add(new_password_hash)
        db.flush()
        return new_password_hash

    def _hash_password(self: Self, password: str) -> None:
        self.salt = str(uuid.uuid4())
        self.algorithm = Algorithm.SHA256

        salted_input = password + self.salt
        hash_object = hashlib.new(self.algorithm.value)
        hash_object.update(salted_input.encode("ascii"))
        self.value = hash_object.hexdigest()
