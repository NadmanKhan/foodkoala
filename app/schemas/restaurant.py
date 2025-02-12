from typing_extensions import Annotated, List

from app.schemas.bases import EntityObjectBase, ObjectBase, Field
from app.schemas.branch import Branch
from app.schemas.item import Item


NameField = Annotated[str, Field(min_length=2, max_length=100)]
DescriptionField = Annotated[str, Field(min_length=0, max_length=500)]


class RestaurantBase(ObjectBase):
    name: NameField
    description: DescriptionField = ""


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(RestaurantBase):
    name: NameField
    description: DescriptionField


class RestaurantAvailable(RestaurantBase, EntityObjectBase):
    branch: Branch
    items: List[Item] = []


class Restaurant(RestaurantBase, EntityObjectBase):
    branches: List[Branch] = []
    items: List[Item] = []
