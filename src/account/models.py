"""Package for account models."""

from __future__ import annotations

import hashlib
import typing
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, select, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from src.account.enums import Algorithm
from src.auth.models import Session as SessionModel
from src.auth.schemas import Credentials
from src.profile.models import Profile
from src.shared.database import Base
from src.shared.exceptions import NotFoundException


if TYPE_CHECKING:
    from typing import Self


class Account(Base):
    """ORM model for 'account' table."""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003

    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    password_hash: Mapped["PasswordHash"] = relationship(uselist=False, back_populates="account")  # noqa: UP037
    profile: Mapped["Profile"] = relationship(uselist=False, back_populates="account")  # noqa: UP037
    sessions: Mapped[list["SessionModel"]] = relationship("Session", back_populates="account")  # noqa: UP037

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

    @classmethod
    def get(cls: type[Account], db: Session, account_id: int) -> Account:
        """Get Account by id."""
        query = select(Account).where(Account.id == account_id)
        row = db.execute(query).one_or_none()
        if row is None:
            msg = "Account not found"
            raise NotFoundException(msg)
        return typing.cast(Account, row.Account)

    @classmethod
    def get_by_credentials(cls: type[Account], credentials: Credentials, db: Session) -> Account:
        """Validate credentials and get an object."""
        query = select(Account).where(Account.email == credentials.email)
        row = db.execute(query).one_or_none()

        if row is None or not row.Account.password_hash.check(credentials.password):
            msg = "Account with provided credentials does not exist."
            raise NotFoundException(msg)

        return typing.cast(Account, row.Account)

    @classmethod
    def get_by_email(cls: type[Account], db: Session, email: str) -> Account:
        """Get Account by e-mail."""
        query = select(Account).where(Account.email == email)
        row = db.execute(query).one_or_none()
        if row is None:
            msg = "Account not found"
            raise NotFoundException(msg)
        return typing.cast(Account, row.Account)

    def has_session(self: Self, session_id: uuid.UUID) -> bool:
        """Check whether or not Account instance has session with specified id."""
        for session in self.sessions:  # noqa: SIM110
            if session.id == session_id:
                return True
        return False

    def create_session(self: Self, db: Session) -> SessionModel:
        """Create Session object."""
        return SessionModel.new_object(db, self.id)


class PasswordHash(Base):
    """ORM model for the 'password_hash' table."""

    __tablename__ = "password_hash"

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), primary_key=True)

    algorithm: Mapped[Algorithm] = mapped_column(Enum(Algorithm, name="algorithm_enum"), nullable=False)
    salt: Mapped[str] = mapped_column(String(36), nullable=False)
    value: Mapped[str] = mapped_column(String(128), nullable=False)

    account: Mapped["Account"] = relationship(back_populates="password_hash")  # noqa: UP037

    @classmethod
    def new_object(cls: type[PasswordHash], db: Session, password: str, account_id: int) -> PasswordHash:
        """Create new PasswordHash object."""
        new_password_hash = PasswordHash(account_id=account_id)
        new_password_hash._hash_password(password)  # noqa: SLF001
        db.add(new_password_hash)
        db.flush()
        return new_password_hash

    def _generate_hash(self: Self, password: str) -> str:
        salted_input = password + self.salt
        hash_object = hashlib.new(self.algorithm.value)
        hash_object.update(salted_input.encode("ascii"))
        return hash_object.hexdigest()

    def _hash_password(self: Self, password: str) -> None:
        self.salt = str(uuid.uuid4())
        self.algorithm = Algorithm.SHA256
        self.value = self._generate_hash(password)

    def check(self: Self, password: str) -> bool:
        """Check whether or not provided value's hash is password hash."""
        password_hash = self._generate_hash(password)
        return password_hash == self.value
