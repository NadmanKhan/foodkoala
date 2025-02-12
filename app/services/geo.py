from math import sin, cos, sqrt, atan2
from typing_extensions import Tuple

from app.config import PROXIMITY_THRESHOLD


def get_distance(coords1: Tuple[float, float], coords2: Tuple[float, float]) -> float:
    """
    Haversine formula to calculate the minimum distance between two points on the Earth's surface.

    Parameters:
    * `coords1`: `Tuple[float, float]` -- Latitude and longitude of the first point, in radians
    * `coords2`: `Tuple[float, float]` -- Latitude and longitude of the second point, in radians

    Returns:
    * `float` -- The distance between the two points, in meters
    """
    lat1, lon1 = coords1
    lat2, lon2 = coords2
    R = 6371000  # radius of the Earth in meters
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c  # distance in meters


def are_near_enough(coords1: Tuple[float, float], coords2: Tuple[float, float]) -> bool:
    return get_distance(coords1, coords2) <= PROXIMITY_THRESHOLD
