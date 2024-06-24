"""Routes for search package."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.auth.dependencies import get_token
from src.auth.schemas import TokenPayload
from src.profile.schemas import Profiles
from src.search import controllers
from src.shared.database import Db
from src.shared.swagga import Description


router = APIRouter(tags=["search"])


@router.get(
    "/search/profiles",
    responses={
        status.HTTP_200_OK: {"description": "Profile info is returned."},
        status.HTTP_401_UNAUTHORIZED: {"description": Description.HTTP_401},
        status.HTTP_403_FORBIDDEN: {"description": Description.HTTP_403},
    },
    response_model=Profiles,
    status_code=status.HTTP_200_OK,
)
def search_profiles(
    db: Db,
    token: Annotated[TokenPayload, Depends(get_token)],  # noqa: ARG001
    profile_username: Annotated[str, Query(example="bob1997")],
    limit: Annotated[int, Query(example=5)],
    offset: Annotated[int, Query(example=5)],
) -> Profiles:
    """Get profiles search result endpoint."""
    return controllers.search_profiles(
        db=db,
        profile_username=profile_username,
        limit=limit,
        offset=offset,
    )
