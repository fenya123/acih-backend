"""Main package for source code."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.account.routes import router as account_router
from src.auth.routes import router as auth_router
from src.entity.routes import router as entity_router
from src.feed.routes import router as feed_router
from src.files.routes import router as files_router
from src.following.routes import router as follower_router
from src.post.routes import router as post_router
from src.profile.routes import router as profile_router
from src.search.routes import router as search_router
from src.shared.exceptions import (
    EntityTooLargeException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    UnsupportedTypeException,
)


if TYPE_CHECKING:
    from fastapi import Request


app = FastAPI()

app.include_router(account_router)
app.include_router(auth_router)
app.include_router(entity_router)
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


@app.exception_handler(UnauthorizedException)
def handle_unauthorized_exception(_: Request, exc: UnauthorizedException) -> JSONResponse:
    """Handle UnauthorizedException."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "description": exc.description,
            "detail": exc.detail,
        },
    )


@app.exception_handler(ForbiddenException)
def handle_forbidden_exception(_: Request, exc: ForbiddenException) -> JSONResponse:
    """Handle ForbiddenException."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "action": exc.action,
            "description": exc.description,
            "detail": exc.detail,
        },
    )


@app.exception_handler(NotFoundException)
def handle_not_found_exception(_: Request, exc: NotFoundException) -> JSONResponse:
    """Handle NotFoundException."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "resource": exc.resource,
            "description": exc.description,
            "detail": exc.detail,
        },
    )


@app.exception_handler(EntityTooLargeException)
def handle_too_large_exception(_: Request, exc: EntityTooLargeException) -> JSONResponse:  # pragma: no cover
    """Handle TooLargeException."""
    return JSONResponse(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        content={
            "resource": exc.resource,
            "description": exc.description,
            "detail": exc.detail,
        },
    )


@app.exception_handler(UnsupportedTypeException)
def handle_unsupported_type_exception(_: Request, exc: UnsupportedTypeException) -> JSONResponse:
    """Handle UnsupportedTypeException."""
    return JSONResponse(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        content={
            "resource": exc.resource,
            "description": exc.description,
            "detail": exc.detail,
        },
    )
