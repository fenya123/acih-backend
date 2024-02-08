"""Controllers for auth package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from src.account.models import Account
from src.auth.models import Session as SessionModel
from src.auth.schemas import Session as SessionSchema
from src.auth.schemas import SessionWithToken, TokenPayload


if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.orm import Session

    from src.auth.schemas import Credentials


def create_session(credentials: Credentials, db: Session) -> SessionWithToken:
    """Create session."""
    account = Account.get_by_credentials(credentials, db)
    session = account.create_session(db)
    payload = TokenPayload(session_id=session.id, account_id=account.id)

    return SessionWithToken(
        session=SessionSchema.model_validate(session, from_attributes=True),
        token=payload.token,
    )


def remove_session(account_id: int, token: TokenPayload, db: Session, session_id: UUID) -> None:
    """Remove session."""
    if token.account_id != account_id or token.session_id != session_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No rights to perform that action")

    session = SessionModel.get(db, session_id)
    session.remove(db)
