from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status as http_status
from jwt import encode, decode
from typing_extensions import Annotated

from app.storage.db import new_db_session
from app.config import JWT_SECRET, JWT_ALGORITHM, API_V1_PREFIX, SESSION_EXPIRE_MINUTES
from app.schemas.auth import AuthToken, JWTPayload
from app.services.user import UserService
from app.schemas.user import User

LoginFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
AccessTokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl=f"{API_V1_PREFIX}/login/access-token"))]

class AuthService:

    @classmethod
    def create_token(cls, form_data: LoginFormDep) -> AuthToken:
        user_service = UserService(new_db_session())
        user = user_service.authenticate_and_get_user(
            email=form_data.username,
            password=form_data.password,
        )
        return AuthToken(
            access_token=cls.encode_username_into_token(username=user.email),
            token_type="bearer",
        )

    @classmethod
    def get_current_user(cls, access_token: AccessTokenDep) -> User:
        email = cls.decode_username_from_token(access_token=access_token)
        return UserService(new_db_session()).get_by_email(email)

    @classmethod
    def encode_username_into_token(cls, *, username: str) -> str:
        payload = JWTPayload(
            sub=username,
            exp=datetime.now(timezone.utc) + timedelta(minutes=SESSION_EXPIRE_MINUTES),
        )
        return encode(payload.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)

    @classmethod
    def decode_username_from_token(cls, *, access_token: str) -> str:
        payload = JWTPayload(**decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM]))
        if payload.exp is not None:
            if datetime.fromtimestamp(payload.exp, timezone.utc) < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=http_status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                )
        return payload.sub

