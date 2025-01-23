from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Tuple


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
    phone: str

    orders: List["Order"] = Relationship(back_populates="user")


class Token(SQLModel):
    access_token: str
    token_type: str


class Area(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    loc_lat: float
    loc_lon: float

    branches: List["Branch"] = Relationship(back_populates="area")


class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    branches: List["Branch"] = Relationship(back_populates="restaurant", cascade_delete=True)
    items: List["Item"] = Relationship(back_populates="restaurant", cascade_delete=True)


class Branch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True, ondelete="CASCADE")
    area_id: Optional[int] = Field(default=None, foreign_key="area.id", index=True, ondelete="SET NULL")
    loc_lat: float
    loc_lon: float

    restaurant: Restaurant = Relationship(back_populates="branches")
    area: Area = Relationship(back_populates="branches")
    orders: List["Order"] = Relationship(back_populates="branch")


class OrderItem(SQLModel, table=True):
    item_id: int = Field(foreign_key="item.id", primary_key=True)
    order_id: int = Field(foreign_key="order.id", primary_key=True)
    quantity: int

    item: "Item" = Relationship(back_populates="order_links_of_item")
    order: "Order" = Relationship(back_populates="item_links_of_order")


class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True, ondelete="CASCADE")
    name: str
    price: float

    restaurant: Restaurant = Relationship(back_populates="items")
    order_links_of_item: List[OrderItem] = Relationship(back_populates="item")


class Order(SQLModel, table=True):
    class Status(str, Enum):
        PENDING = "pending"
        ACCEPTED = "accepted"
        PICKEDUP = "pickedup"
        DELIVERED = "delivered"

        REJECTED = "rejected"
        CANCELLED = "cancelled"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    branch_id: int = Field(foreign_key="branch.id", index=True)
    date: datetime
    loc_lat: float
    loc_lon: float
    status: Status = Field(default=Status.PENDING, index=True)

    user: User = Relationship(back_populates="orders")
    branch: Branch = Relationship(back_populates="orders")
    item_links_of_order: List[OrderItem] = Relationship(back_populates="order")
