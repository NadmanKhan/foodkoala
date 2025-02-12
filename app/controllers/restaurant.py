from fastapi import APIRouter, Depends
from typing_extensions import Annotated, List, Optional

from app.schemas import Restaurant, RestaurantCreate, RestaurantUpdate, RestaurantAvailable
from app.services import RestaurantService

restaurant_router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"],
)

RestaurantServiceDep = Annotated[RestaurantService, Depends()]


@restaurant_router.get("/", response_model=List[Restaurant])
async def get_restaurants(
    restaurant_service: RestaurantServiceDep, offset: Optional[int] = None, limit: Optional[int] = None
):
    return restaurant_service.get_list(offset=offset, limit=limit)


@restaurant_router.get("/available", response_model=List[RestaurantAvailable])
async def get_available_restaurants(delivery_coords: tuple, restaurant_service: RestaurantServiceDep):
    return restaurant_service.get_available_list(delivery_coords=delivery_coords)


@restaurant_router.get("/{restaurant_id}", response_model=Restaurant)
async def get_restaurant(restaurant_service: RestaurantServiceDep, restaurant_id: int):
    return restaurant_service.get(id=restaurant_id)


@restaurant_router.post("/", response_model=Restaurant)
async def create_restaurant(restaurant_service: RestaurantServiceDep, data: RestaurantCreate):
    return restaurant_service.create(data=data)


@restaurant_router.put("/{restaurant_id}", response_model=Restaurant)
async def update_restaurant(restaurant_service: RestaurantServiceDep, restaurant_id: int, data: RestaurantUpdate):
    return restaurant_service.update(id=restaurant_id, data=data)


@restaurant_router.delete("/{restaurant_id}", response_model=Restaurant)
async def delete_restaurant(restaurant_service: RestaurantServiceDep, restaurant_id: int):
    return restaurant_service.delete(id=restaurant_id)
