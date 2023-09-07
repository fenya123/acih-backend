"""Main package for source code."""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    """Return 'Hello World'."""
    return {"message": "Hello World"}
