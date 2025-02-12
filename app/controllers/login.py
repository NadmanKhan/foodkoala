from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing_extensions import Annotated, List, Optional

from app.schemas import AuthToken, User
from app.services.auth import AuthService

login_router = APIRouter(
    prefix="/login",
    tags=["login"],
)


@login_router.post("/access-token", response_model=AuthToken)
async def login_for_access_token(auth_token: Annotated[AuthToken, Depends(AuthService.create_token)]):
    return auth_token


@login_router.post("/test-token", response_model=User)
async def test_token(user: Annotated[User, Depends(AuthService.get_current_user)]):
    return user

