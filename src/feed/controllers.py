"""Controllers for 'feed' package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.account.models import Account
from src.post.models import Post
from src.post.schemas import Posts


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def get_followed_posts_feed(
    db: Session, account_id: int, limit: int, offset: int,
) -> Posts:
    """Get followed posts for an account."""
    account = Account.get(db, account_id)
    posts = account.get_followed_posts(db=db, limit=limit, offset=offset)

    return Posts(posts=posts)


def get_suggested_posts_feed(
    db: Session, limit: int, offset: int,
) -> Posts:
    """Get suggested posts."""
    posts = Post.get_suggested_posts(db=db, limit=limit, offset=offset)

    return Posts(posts=posts)
