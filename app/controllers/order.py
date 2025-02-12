from fastapi import APIRouter, Depends
from typing_extensions import Annotated, List, Optional

from app.schemas import Order, OrderCreate, OrderUpdate
from app.services import OrderService

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

OrderServiceDep = Annotated[OrderService, Depends()]


@order_router.get("/", response_model=List[Order])
async def get_orders(order_service: OrderServiceDep, offset: Optional[int] = None, limit: Optional[int] = None):
    return order_service.get_list(offset=offset, limit=limit)


@order_router.get("/{order_id}", response_model=Order)
async def get_order(order_service: OrderServiceDep, order_id: int):
    return order_service.get(id=order_id)


@order_router.post("/", response_model=Order)
async def create_order(order_service: OrderServiceDep, data: OrderCreate):
    return order_service.create(data=data)


@order_router.put("/{order_id}", response_model=Order)
async def update_order(order_service: OrderServiceDep, order_id: int, data: OrderUpdate):
    return order_service.update(id=order_id, data=data)


@order_router.delete("/{order_id}", response_model=Order)
async def delete_order(order_service: OrderServiceDep, order_id: int):
    return order_service.delete(id=order_id)
