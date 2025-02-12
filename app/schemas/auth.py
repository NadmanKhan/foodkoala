from datetime import datetime
from typing_extensions import Optional

from app.schemas.bases import ObjectBase


class AuthToken(ObjectBase):
    """
    Authentication token
    """

    access_token: str
    token_type: str = "bearer"


class JWTPayload(ObjectBase):
    """
    Contents of JWT token
    """

    sub: Optional[str] = None
    exp: Optional[datetime] = None
