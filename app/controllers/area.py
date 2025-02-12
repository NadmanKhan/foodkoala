from fastapi import APIRouter, Depends
from typing_extensions import Annotated, List, Optional

from app.schemas import Area, AreaCreate, AreaUpdate
from app.services import AreaService

area_router = APIRouter(
    prefix="/areas",
    tags=["areas"],
)

AreaServiceDep = Annotated[AreaService, Depends()]


@area_router.get("/", response_model=List[Area])
async def get_areas(area_service: AreaServiceDep, offset: Optional[int] = None, limit: Optional[int] = None):
    return area_service.get_list(offset=offset, limit=limit)


@area_router.get("/{area_id}", response_model=Area)
async def get_area(area_service: AreaServiceDep, area_id: int):
    return area_service.get(id=area_id)


@area_router.post("/", response_model=Area)
async def create_area(area_service: AreaServiceDep, data: AreaCreate):
    return area_service.create(data=data)


@area_router.put("/{area_id}", response_model=Area)
async def update_area(area_service: AreaServiceDep, area_id: int, data: AreaUpdate):
    return area_service.update(id=area_id, data=data)


@area_router.delete("/{area_id}", response_model=Area)
async def delete_area(area_service: AreaServiceDep, area_id: int):
    return area_service.delete(id=area_id)
