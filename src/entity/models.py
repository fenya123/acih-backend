"""Package for entity models."""

from __future__ import annotations

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.database import Base


class Entity(Base):  # pylint: disable=too-few-public-methods
    """Mock class for checking database connectivity."""

    __tablename__ = "entity"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003
