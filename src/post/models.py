"""Package for post models."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import DateTime, desc, ForeignKey, func, Integer, select, String
from sqlalchemy.orm import Mapped, mapped_column, Session

from src.post.schemas import Post as PostSchema
from src.post.schemas import PostContent
from src.shared.database import Base
from src.shared.datetime import utcnow


class Post(Base):
    """ORM model of 'post' table."""

    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)  # noqa: A003

    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True, unique=False)
    file_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False, unique=True)
    preview_id: Mapped[int] = mapped_column(ForeignKey("file.id"), nullable=False, unique=True)
    title: Mapped[str | None] = mapped_column(String(100), nullable=True, unique=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

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

    @classmethod
    def get_suggested_posts(cls: type[Post], db: Session, limit: int, offset: int) -> list[PostSchema]:
        """Get suggested posts for an account."""
        row_num_subquery = (
            select(
                Post.id.label("post_id"),
                func.row_number()
                .over(partition_by=Post.account_id, order_by=desc(Post.created_at))  # type: ignore[no-untyped-call]
                .label("row_num"),
            )
            .select_from(Post)
            .where(datetime.now(tz=timezone.utc) - (Post.created_at) <= timedelta(days=7))
            .subquery()
        )

        query = (
            select(
                Post,
            )
            .select_from(Post)
            .join(row_num_subquery, Post.id == row_num_subquery.c.post_id)
            .where(row_num_subquery.c.row_num <= 3)  # noqa: PLR2004
            .order_by(Post.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        rows = db.execute(query).all()
        return [PostSchema.model_validate(row.Post, from_attributes=True) for row in rows]
