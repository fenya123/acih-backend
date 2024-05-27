"""Package for post models."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, Session

from src.post.schemas import PostContent
from src.shared.database import Base


class Post(Base):  # pylint: disable=too-few-public-methods
    """ORM model of 'post' table."""

    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True, unique=False)
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False, unique=True)
    preview_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False, unique=True)
    title: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=False)

    @classmethod
    def new_object(
        cls: type[Post],
        db: Session,
        account_id: int,
        preview_id: int,
        post_content: PostContent,
    ) -> Post:
        """Create a new post object."""
        post = Post(
            account_id=account_id,
            description=post_content.description,
            file_id=post_content.file_id,
            preview_id=preview_id,
            title=post_content.title,
        )

        db.add(post)
        db.flush()
        return post
