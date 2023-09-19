"""Main package for source code."""

from __future__ import annotations

from fastapi import FastAPI

from src.entity.routes import router as entity_router


app = FastAPI()

app.include_router(entity_router)


@app.get("/")
def root() -> dict[str, str]:
    """Return 'Hello World'."""
    return {"message": "Hello World"}
