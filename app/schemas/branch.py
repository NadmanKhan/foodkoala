from typing_extensions import Optional

from app.schemas.bases import ObjectBase, EntityObjectBase, LocatableBase, LocatableUpdateBase, IdField


class BranchBase(LocatableBase, ObjectBase):
    restaurant_id: IdField
    area_id: Optional[int] = None


class BranchCreate(BranchBase):
    pass


class BranchUpdate(LocatableUpdateBase, BranchBase):
    restaurant_id: IdField = None
    area_id: int = None


class Branch(BranchBase, EntityObjectBase):
    pass
