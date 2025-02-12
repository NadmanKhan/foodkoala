from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from math import radians
from pydantic import validate_email
from sqlmodel import col, select, Session
from typing import List, Optional
from typing_extensions import Annotated

from .config import API_V1_PREFIX
from .storage.mappers import new_db_session, Area, User, Restaurant, Branch, Order, Token
from .utilities import (
    haversine,
    in_range,
    process_order,
    hash_password,
    verify_user,
    create_access_token,
    get_user_from_token,
)

router = APIRouter(prefix=API_V1_PREFIX)


@router.post("/signup/")
async def sign_up(user: User) -> User:
    with new_db_session() as db:
        # Check if the user already exists
        existing_user = db.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        # Check if the email is valid
        try:
            validate_email(user.email)
        except:
            raise HTTPException(status_code=400, detail="Invalid email address")

        # Check if the password is strong enough
        if len(user.password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
        if not any(c.isupper() for c in user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
        if not any(c.islower() for c in user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in user.password):
            raise HTTPException(status_code=400, detail="Password must contain at least one digit")

        # Create and save the user
        user.password = hash_password(user.password)

        user.id = None
        db.add(user)
        db.commit()
        db.refresh(user)

        # Remove the password from the response before returning
        del user.password
        return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{router.prefix}/login/")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/login/")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # Authenticate the user
    if not verify_user(form_data.username, form_data.password):
        raise credentials_exception

    # Get the user
    user: Optional[User] = None
    with new_db_session() as db:
        user = db.exec(select(User).where(User.email == form_data.username)).first()
    assert user is not None

    # Create and return the access token
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = get_user_from_token(token)
    if user is None:
        raise credentials_exception
    return user


@router.get("/orders/")
async def read_orders_of_current_user(user: Annotated[User, Depends(get_current_user)]):
    with new_db_session() as db:
        return db.exec(select(Order).where(Order.user_id == user.id)).all()


@router.post("/orders/")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    with new_db_session() as db:
        order.id = None

        # Find the nearest 4 areas to the order location
        areas = db.exec(select(Area)).all()
        areas = sorted(areas, key=lambda area: haversine(area.loc_lat, area.loc_lon, order.loc_lat, order.loc_lon))
        areas = areas[:4]

        # Get the branches in these 4 areas
        branches = db.exec(select(Branch).where(col(Branch.area_id).in_([area.id for area in areas]))).all()

        # Filter branches that are too far (more than 5 km) away
        branches = [
            branch for branch in branches if in_range(order.loc_lat, order.loc_lon, branch.loc_lat, branch.loc_lon)
        ]

        # If the order is not in any of the branches, reject the order
        if order.branch_id not in [branch.id for branch in branches]:
            order.status = Order.Status.REJECTED
            return order

        # Otherwise, save and process the order
        order.status = Order.Status.PENDING
        db.add(order)
        db.commit()
        db.refresh(order)

        # Process the order in the background
        background_tasks.add_task(process_order, order)

        return order


@router.get("/areas/")
async def read_areas():
    with new_db_session() as db:
        return db.exec(select(Area)).all()


@router.get("/restaurants/")
async def read_restaurants(lat: Optional[float] = None, lon: Optional[float] = None, in_radians: Optional[bool] = None):
    with new_db_session() as db:
        restaurants = db.exec(select(Restaurant)).all()

        # Filter the branches based on the location
        # and remove the restaurants that have no branches left
        if lat is not None and lon is not None:
            if in_radians is None or not in_radians:
                lat = radians(lat)
                lon = radians(lon)
            for r in restaurants:
                r.branches = [b for b in r.branches if in_range(lat, lon, b.loc_lat, b.loc_lon)]
            restaurants = [r for r in restaurants if r.branches]

        return restaurants


def closest_areas(lat: float, lon: float, n: int):
    with new_db_session() as db:
        areas = db.exec(select(Area)).all()
        areas = sorted(areas, key=lambda area: haversine(area.loc_lat, area.loc_lon, lat, lon))
        return areas[:n]


@router.get("/restaurants/")
async def read_restaurants(lat: float, lon: float):
    with new_db_session() as db:

        # Find the nearest 4 areas to the location
        areas = closest_areas(lat, lon, 4)

        # Get the branches in these 4 areas and the restaurants they belong to
        restaurants = db.exec(
            select(Restaurant).join(Branch).where(col(Area.id).in_([area.id for area in areas]))
        ).all()

        # Filter branches that are too far away
        for r in restaurants:
            r.branches = [branch for branch in r.branches if in_range(lat, lon, branch.loc_lat, branch.loc_lon)]

        return restaurants


@router.get("/restaurants/{restaurant_id}")
async def read_restaurant(restaurant_id: int):
    with new_db_session() as db:
        return db.get(Restaurant, restaurant_id)
