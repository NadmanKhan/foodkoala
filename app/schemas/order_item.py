from typing_extensions import Annotated, Optional

from app.schemas.bases import ObjectBase, Field, IdField


QuantityField = Annotated[int, Field(gt=0)]


class OrderItemBase(ObjectBase):
    order_id: IdField
    item_id: IdField
    quantity: QuantityField


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(OrderItemBase):
    order_id: IdField = None
    item_id: IdField = None
    quantity: QuantityField = None


class OrderItem(OrderItemBase, ObjectBase):
    pass
