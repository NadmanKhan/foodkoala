from typing_extensions import List, Tuple

from app.schemas.area import Area, AreaCreate, AreaUpdate
from app.storage.mappers import AreaMapper, select
from app.services.mixins import EntityCRUDMixin
from app.services.geo import get_distance


class AreaService(EntityCRUDMixin[Area, AreaCreate, AreaUpdate, AreaMapper]):

    def get_nearby_list(self, *, coords: Tuple[float, float], radius: float, limit: int = 10) -> List[Area]:
        areas = self.db.exec(select(AreaMapper)).all()
        areas = sorted(areas, key=lambda area: get_distance(area.coords, coords))
        areas = [area for area in areas if get_distance(area.coords, coords) <= radius]
        return areas[: max(0, min(limit, len(areas)))]
