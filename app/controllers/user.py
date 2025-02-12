from fastapi import APIRouter, Depends
from typing_extensions import Annotated, List, Optional

from app.schemas import User, UserCreate, UserUpdate
from app.services import UserService, AuthService

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

UserServiceDep = Annotated[UserService, Depends()]

CurrentUserDep = Annotated[User, Depends(AuthService.get_current_user)]


@user_router.get("/", response_model=List[User])
async def get_users(user_service: UserServiceDep, offset: Optional[int] = None, limit: Optional[int] = None):
    return user_service.get_list(offset=offset, limit=limit)


@user_router.get("/{user_id}", response_model=User)
async def get_user(user_service: UserServiceDep, user_id: int):
    return user_service.get(id=user_id)


@user_router.get("/me", response_model=User)
async def get_me(current_user: CurrentUserDep):
    return current_user


@user_router.post("/", response_model=User)
async def create_user(user_service: UserServiceDep, data: UserCreate):
    return user_service.create(data=data)


@user_router.put("/{user_id}", response_model=User)
async def update_user(user_service: UserServiceDep, user_id: int, data: UserUpdate):
    return user_service.update(id=user_id, data=data)


@user_router.delete("/{user_id}", response_model=User)
async def delete_user(user_service: UserServiceDep, user_id: int):
    return user_service.delete(id=user_id)
