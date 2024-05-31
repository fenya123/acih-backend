"""Controllers for post package endpoints."""

from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING

from src.account.models import Account
from src.files.image_processor import ImageProcessor
from src.files.models import File
from src.post.schemas import Post, Posts
from src.shared.storage import Minio


if TYPE_CHECKING:
    from pathlib import Path

    from fastapi import BackgroundTasks
    from sqlalchemy.orm import Session

    from src.auth.schemas import TokenPayload
    from src.post.schemas import PostContent


def create_post(
    db: Session,
    token: TokenPayload,
    post_content: PostContent,
    background_tasks: BackgroundTasks,
    tmp_dir: Path,
) -> Post:
    """Create a post."""
    file = File.get(db, post_content.file_id)

    image_processor = ImageProcessor(file, tmp_dir)
    preview_path = image_processor.create_preview()

    preview = file.generate_preview(db=db, size=os.path.getsize(preview_path))

    minio = Minio.get_client()
    minio.fput_object(
        bucket_name="files",
        object_name=str(preview.id),
        file_path=preview_path,
    )

    account = Account.get(db, token.account_id)
    post = account.add_post(db=db, preview_id=preview.id, post_content=post_content)

    background_tasks.add_task(shutil.rmtree, tmp_dir)
    return Post.model_validate(post, from_attributes=True)


def get_post(db: Session, account_id: int, post_id: int) -> Post:
    """Get post."""
    account = Account.get(db, account_id)

    return account.get_post(db, post_id)


def get_posts(db: Session, account_id: int, limit: int, offset: int) -> Posts:
    """Get a list of user's posts."""
    account = Account.get(db, account_id)
    posts = account.get_posts(db=db, limit=limit, offset=offset)

    return Posts(posts=posts)
