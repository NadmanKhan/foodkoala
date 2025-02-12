from pydantic import BaseModel, Field
from typing_extensions import Annotated, Optional, Tuple


class ObjectBase(BaseModel):
    """
    Base class for all objects in the application's domain model. Inherited from
    Pydantic's `BaseModel` class to provide validation and serialization capabilities.
    """

    pass


IdField = Annotated[int, Field(ge=0)]


class EntityObjectBase(ObjectBase):
    """
    Base class for all entities in the application's domain model. Inherited from
    the `DomainObject` class. It has an `id` field that is used to uniquely identify
    the entity.
    """

    id: IdField


AddressField = Annotated[str, Field(min_length=0, max_length=200)]


class LocatableBase(ObjectBase):
    """
    Base class for all objects that have a location.
    """

    latitude: float
    longitude: float
    address: AddressField = ""

    @property
    def coords(self) -> Tuple[float, float]:
        return self.latitude, self.longitude

    @coords.setter
    def coords(self, value: Tuple[float, float]):
        self.latitude, self.longitude = value


class LocatableUpdateBase(LocatableBase):
    """
    Base class for all objects that have an optional location.
    """

    latitude: float = None
    longitude: float = None
    address: AddressField = None

    @property
    def coords(self) -> Optional[Tuple[float, float]]:
        if self.latitude is not None and self.longitude is not None:
            return self.latitude, self.longitude
        return None

    @coords.setter
    def coords(self, value: Optional[Tuple[float, float]]):
        if value is not None:
            self.latitude, self.longitude = value
        else:
            self.latitude = self.longitude = None
