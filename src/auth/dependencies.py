"""Fastapi dependencies for auth feature."""

from __future__ import annotations

from typing import Annotated  # noqa: TCH003

from fastapi import Depends  # noqa: TCH002
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer  # noqa: TCH002
from jwt.exceptions import InvalidSignatureError

from src.account.models import Account
from src.auth.exceptions import InvalidTokenException
from src.auth.schemas import TokenPayload
from src.shared.database import Db  # noqa: TCH001
from src.shared.exceptions import NotFoundException


bearer = HTTPBearer()


def get_token(
    token: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    db: Db,
) -> TokenPayload:
    """Validate authorization token."""
    try:
        payload = TokenPayload.from_token(token.credentials)
    except InvalidSignatureError:
        # pylint: disable-next=raise-missing-from
        raise InvalidTokenException  # noqa: B904

    try:
        account = Account.get(db, account_id=payload.account_id)
    except NotFoundException:
        # pylint: disable-next=raise-missing-from
        raise InvalidTokenException  # noqa: B904

    if not account.has_session(session_id=payload.session_id):
        raise InvalidTokenException

    return payload
