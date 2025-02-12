from typing_extensions import List
from enum import Enum

from app.schemas.bases import ObjectBase, EntityObjectBase, LocatableBase, LocatableUpdateBase, IdField
from app.schemas.order_item import OrderItem


class OrderStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    PICKEDUP = "pickedup"
    DELIVERED = "delivered"

    REJECTED = "rejected"
    CANCELLED = "cancelled"


class OrderBase(LocatableBase, ObjectBase):
    customer_id: IdField
    branch_id: IdField


class OrderCreate(OrderBase):
    pass


class OrderUpdate(LocatableUpdateBase, OrderBase):
    customer_id: IdField = None
    branch_id: IdField = None
    status: OrderStatus = None
    item_links: List[OrderItem] = []


class Order(OrderBase, EntityObjectBase):
    item_links: List[OrderItem] = []
