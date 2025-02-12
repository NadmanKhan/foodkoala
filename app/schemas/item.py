from typing_extensions import Annotated

from app.schemas.bases import ObjectBase, EntityObjectBase, Field, IdField

NameField = Annotated[str, Field(min_length=2, max_length=100)]
DescriptionField = Annotated[str, Field(min_length=0, max_length=500)]
PriceField = Annotated[float, Field(gt=0)]


class ItemBase(ObjectBase):
    name: NameField
    description: DescriptionField
    price: PriceField
    restaurant_id: IdField


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    name: NameField = None
    description: DescriptionField = None
    price: PriceField = None
    restaurant_id: IdField = None


class Item(ItemBase, EntityObjectBase):
    pass
