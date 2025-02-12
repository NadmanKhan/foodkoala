from datetime import datetime
import re
from sqlmodel import Field, Relationship, SQLModel, delete, select, col as column, text as sqltext, update
from typing_extensions import Optional, List

from app.schemas import AreaBase, BranchBase, ItemBase, OrderBase, OrderStatus, OrderItemBase, RestaurantBase, UserBase

_camel_case_pattern = re.compile(r"(?<!^)(?=[A-Z])")


class MapperBase(SQLModel):
    """
    Base class for all mappers, giving them all a proper `__tablename__` attribute.
    """

    @classmethod
    def __init_subclass__(cls, **kwargs):
        if kwargs.get("table", False):
            # make snake_case table name from class name, without the "Mapper" suffix
            cls.__tablename__ = _camel_case_pattern.sub("_", cls.__name__).lower().replace("_mapper", "")
        super().__init_subclass__(**kwargs)


class EntityMapperBase(MapperBase):
    """
    Base class for mappers of all entities in the database, providing common fields like
    `id`, `created_at`, and `updated_at`.
    """

    id: Optional[int] = Field(None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(None)


class UserMapper(EntityMapperBase, UserBase, table=True):
    __tablename__ = "user"
    email: str = Field(index=True, unique=True)
    hashed_password: str
    orders: List["OrderMapper"] = Relationship(back_populates="customer", cascade_delete=True)


class AreaMapper(EntityMapperBase, AreaBase, table=True):
    __tablename__ = "area"
    branches: List["BranchMapper"] = Relationship(back_populates="area", cascade_delete=False)


class RestaurantMapper(EntityMapperBase, RestaurantBase, table=True):
    __tablename__ = "restaurant"
    branches: List["BranchMapper"] = Relationship(back_populates="restaurant", cascade_delete=True)
    items: List["ItemMapper"] = Relationship(back_populates="restaurant", cascade_delete=True)


class BranchMapper(EntityMapperBase, BranchBase, table=True):
    __tablename__ = "branch"
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True, ondelete="CASCADE")
    restaurant: RestaurantMapper = Relationship(back_populates="branches")

    area_id: Optional[int] = Field(None, foreign_key="area.id", index=True, ondelete="SET NULL")
    area: AreaMapper = Relationship(back_populates="branches")

    orders: List["OrderMapper"] = Relationship(back_populates="branch", cascade_delete=True)


class ItemMapper(EntityMapperBase, ItemBase, table=True):
    __tablename__ = "item"
    restaurant_id: int = Field(foreign_key="restaurant.id", index=True, ondelete="CASCADE")
    restaurant: RestaurantMapper = Relationship(back_populates="items")

    order_links: List["OrderItemMapper"] = Relationship(back_populates="item", cascade_delete=True)


class OrderMapper(EntityMapperBase, OrderBase, table=True):
    __tablename__ = "order"
    customer_id: int = Field(foreign_key="user.id", index=True, ondelete="CASCADE")
    customer: UserMapper = Relationship(back_populates="orders")
    status: OrderStatus = Field(index=True)

    branch_id: int = Field(foreign_key="branch.id", index=True, ondelete="CASCADE")
    branch: BranchMapper = Relationship(back_populates="orders")

    item_links: List["OrderItemMapper"] = Relationship(back_populates="order", cascade_delete=True)


class OrderItemMapper(MapperBase, OrderItemBase, table=True):
    __tablename__ = "order_item"
    item_id: int = Field(foreign_key="item.id", primary_key=True, ondelete="CASCADE")
    item: ItemMapper = Relationship(back_populates="order_links")

    order_id: int = Field(foreign_key="order.id", primary_key=True, ondelete="CASCADE")
    order: OrderMapper = Relationship(back_populates="item_links")
