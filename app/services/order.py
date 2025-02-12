from fastapi import HTTPException, status as http_status

from app.schemas.order import Order, OrderCreate, OrderUpdate
from app.storage.mappers import OrderMapper, BranchMapper
from app.services.mixins import EntityCRUDMixin
from app.services.geo import are_near_enough
from app.utilities import overrides


class OrderService(EntityCRUDMixin[Order, OrderCreate, OrderUpdate, OrderMapper]):

    @overrides(EntityCRUDMixin)
    def create(self, *, data: OrderCreate) -> Order:
        branch = self.db.get(BranchMapper, data.branch_id)
        if not are_near_enough(branch.coords, data.coords):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="Order is too far from the branch",
            )
        return super().create(data)
