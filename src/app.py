"""Main package for source code."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.account.routes import router as account_router
from src.auth.routes import router as auth_router
from src.feed.routes import router as feed_router
from src.files.routes import router as files_router
from src.following.routes import router as follower_router
from src.post.routes import router as post_router
from src.profile.routes import router as profile_router
from src.search.routes import router as search_router
from src.shared.exceptions import NotFoundException


if TYPE_CHECKING:
    from fastapi import Request


app = FastAPI(
    title="ACIH API",
    description="Backend API for Artist Centered Image Hosting.",
    openapi_tags=[
        {
            "name": "account",
            "description": "Account-related functionality for managing accounts.",
        },
        {
            "name": "auth",
            "description": "Auth-related functionality for Signing Up/In/Out.",
        },
        {
            "name": "feed",
            "description": "Feed/suggested posts related functionality.",
        },
        {
            "name": "files",
            "description": "Files related functionality for downloading and uploading files.",
        },
        {
            "name": "following",
            "description": "Functionality related to realtionships between accounts.",
        },
        {
            "name": "post",
            "description": "Functionality related to posts.",
        },
        {
            "name": "profile",
            "description": "Profile related functionality for managing profiles.",
        },
        {
            "name": "search",
            "description": "Search related functionality.",
        },
    ],
)

app.include_router(account_router)
app.include_router(auth_router)
app.include_router(feed_router)
app.include_router(files_router)
app.include_router(follower_router)
app.include_router(post_router)
app.include_router(profile_router)
app.include_router(search_router)


@app.get("/")
def root() -> dict[str, str]:
    """Return 'Hello World'."""
    return {"message": "Hello World"}


@app.exception_handler(NotFoundException)
def handle_not_found_exception(_: Request, exc: NotFoundException) -> JSONResponse:
    """Handle NotFoundException."""
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": exc.detail})
