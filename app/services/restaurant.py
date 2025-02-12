from typing_extensions import List, Tuple

from app.schemas.restaurant import Branch, Restaurant, RestaurantCreate, RestaurantUpdate, RestaurantAvailable
from app.storage.mappers import RestaurantMapper, BranchMapper, select, column
from app.storage.db import new_db_session
from app.services.mixins import EntityCRUDMixin
from app.services.area import AreaService
from app.services.geo import get_distance, are_near_enough, PROXIMITY_THRESHOLD


class RestaurantService(EntityCRUDMixin[Restaurant, RestaurantCreate, RestaurantUpdate, RestaurantMapper]):

    def get_available_list(self, *, delivery_coords: Tuple[float, float]) -> List[RestaurantAvailable]:

        # Get nearby areas
        nearby_areas = AreaService(self.db).get_nearby_list(
            coords=delivery_coords,
            radius=PROXIMITY_THRESHOLD,
            limit=4,
        )

        # Get restaurants from branches within nearby areas
        restaurants_rows = self.db.exec(
            select(RestaurantMapper)
            .join(BranchMapper)
            .where(column(BranchMapper.area_id).in_([area.id for area in nearby_areas]))
        ).all()

        # Get the closest branch for each restaurant and check if it is serviceable
        output: list[RestaurantAvailable] = []
        for row in restaurants_rows:
            if not row.branches:
                continue
            closest_branch_row = min(
                row.branches,
                key=lambda branch: get_distance(branch.coords, delivery_coords),
            )
            if are_near_enough(closest_branch_row.coords, delivery_coords):
                branch = Branch.model_validate(closest_branch_row)
                output.append(
                    RestaurantAvailable(
                        **row.model_dump(exclude={"branches"}),
                        branch=branch,
                    )
                )

        return output
