"""Controllers for auth package endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.account.models import Account
from src.auth.schemas import Session as SessionSchema
from src.auth.schemas import SessionWithToken, TokenPayload


if TYPE_CHECKING:
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
