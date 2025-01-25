from datetime import datetime, timedelta, timezone
from jwt import encode, decode
from math import sqrt, sin, cos, atan2
from passlib.context import CryptContext
from sqlmodel import select, Session
from time import sleep
from typing import Optional

from .models import Order, User
from .db import engine
from .settings import SECRET

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Parameters:
    * `password`: `str` -- The password to hash

    Returns:
    * `str` -- The hashed password
    """
    return _pwd_context.hash(password)


def verify_user(email: str, password: str) -> bool:
    """
    Verify a user's email and password.

    Parameters:
    * `email`: `str` -- The email of the user
    * `password`: `str` -- The password of the user

    Returns:
    * `bool` -- `True` if the email and password match, `False` otherwise
    """
    with Session(engine()) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user is None:
            return False
        return _pwd_context.verify(password, user.password)


def create_access_token(email: str) -> str:
    """
    Create a JWT access token using the user's email.

    Parameters:
    * `email`: `str` -- The email of the user

    Returns:
    * `str` -- The JWT access token
    """
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=3600),
    }
    return encode(payload, SECRET, algorithm="HS256")


def get_user_from_token(token: str) -> Optional[User]:
    """
    Get the user from a JWT access token.

    Parameters:
    * `token`: `str` -- The JWT access token

    Returns:
    * `User` -- The user object
    """
    try:
        payload: dict[str, str] = decode(token, SECRET, algorithms=["HS256"])
        user_email: str = payload.get("sub")
        if user_email is None:
            return None
        with Session(engine()) as session:
            return session.exec(select(User).where(User.email == user_email)).first()
    except:
        return None


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Haversine formula to calculate the minimum distance between two points on the Earth's surface.

    Parameters:
    * `lat1`: `float` -- Latitude of the first point, in radians
    * `lon1`: `float` -- Longitude of the first point, in radians
    * `lat2`: `float` -- Latitude of the second point, in radians
    * `lon2`: `float` -- Longitude of the second point, in radians

    Returns:
    * `float` -- The distance between the two points, in meters
    """
    R = 6371000  # radius of the Earth in meters
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # distance in meters


def in_range(lat_src: float, lon_src: float, lat_dst: float, lon_dst: float) -> bool:
    """
    Check if two points are within the allowed distance for delivery.

    Parameters:
    * `lat_src`: `float` -- Latitude of the source point
    * `lon_src`: `float` -- Longitude of the source point
    * `lat_dst`: `float` -- Latitude of the destination point
    * `lon_dst`: `float` -- Longitude of the destination point

    Returns:
    * `bool` -- `True` if the points are within the allowed distance, `False` otherwise
    """
    return haversine(lat_src, lon_src, lat_dst, lon_dst) <= 5000


def process_order(order: Order):
    """
    Process an order and update the stock of the items in the order.

    Parameters:
    * `order`: `Order` -- The order to process

    Returns:
    * `None`
    """

    assert order.status == Order.Status.PENDING, "Order is not pending"

    with Session(engine()) as session:
        for seconds, status in [
            (15, Order.Status.ACCEPTED),
            (30, Order.Status.PICKEDUP),
            (60, Order.Status.DELIVERED),
        ]:
            sleep(seconds)
            if order.status == Order.Status.CANCELLED:
                return
            order.status = status
            session.add(order)
            session.commit()
