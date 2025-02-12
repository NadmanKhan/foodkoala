from typing_extensions import Annotated, List

from app.schemas.bases import ObjectBase, EntityObjectBase, LocatableBase, LocatableUpdateBase, Field
from app.schemas.branch import Branch


NameField = Annotated[str, Field(min_length=2, max_length=100)]


class AreaBase(LocatableBase, ObjectBase):
    name: NameField


class AreaCreate(AreaBase):
    pass


class AreaUpdate(LocatableUpdateBase, AreaBase):
    name: NameField = None


class Area(AreaBase, EntityObjectBase):
    branches: List[Branch] = []
