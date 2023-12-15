"""Main package for source code."""

from __future__ import annotations

from fastapi import FastAPI

from src.account.routes import router as account_router
from src.auth.routes import router as auth_router
from src.entity.routes import router as entity_router
from src.following.routes import router as follower_router
from src.minio.routes import router as minio_router
from src.post.routes import router as post_router
from src.profile.routes import router as profile_router


app = FastAPI()

app.include_router(account_router)
app.include_router(auth_router)
app.include_router(entity_router)
app.include_router(follower_router)
app.include_router(minio_router)
app.include_router(post_router)
app.include_router(profile_router)


@app.get("/")
def root() -> dict[str, str]:
    """Return 'Hello World'."""
    return {"message": "Hello World"}
