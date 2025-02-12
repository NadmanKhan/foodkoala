from abc import ABC, abstractmethod
from datetime import datetime
from fastapi import Depends
from typing_extensions import Annotated, Generic, List, Optional, Type, TypeVar, get_args


from app.schemas.bases import EntityObjectBase, ObjectBase, IdField
from app.services.error import NotFoundHTTPException
from app.storage.mappers import EntityMapperBase, column, select
from app.storage.db import DBSession, new_db_session
from app.config import API_RESOURCE_QUERY_PAGE_MAX


_TEntityType = TypeVar("_TEntityType", bound=EntityObjectBase)
_TCreateType = TypeVar("_TCreateType", bound=ObjectBase)
_TUpdateType = TypeVar("_TUpdateType", bound=ObjectBase)
_TMapperType = TypeVar("_TMapperType", bound=EntityMapperBase)


class EntityCRUDMixin(Generic[_TEntityType, _TCreateType, _TUpdateType, _TMapperType], ABC):
    """
    Generic mixin for all CRUD services in the application. This mixin provides the basic CRUD
    operations for an entity, including getting, creating, updating, and deleting entities.

    The following type hints are required for the subclass:

    * `_TEntityType` --
    The type of entity that the CRUD service is responsible for, as output to the client

    * `_TCreateType` --
    The type of validation object used to create an entity, as input by the client

    * `_TUpdateType` --
    The type of validation object used to update an entity, as input by the client

    * `_TMapperType` --
    The ORM mapper class that maps the entity to the database
    """

    EntityType: Type[_TEntityType]
    CreateType: Type[_TCreateType]
    UpdateType: Type[_TUpdateType]
    MapperType: Type[_TMapperType]

    # Class methods
    # -------------

    def __init_subclass__(
        cls,
        *args,
        **kwargs,
    ):
        """
        Validate that the `CRUDService` subclass has exactly 4 type hints and that they
        are of the correct types, and register them as corresponding class attributes.
        """
        super().__init_subclass__(*args, **kwargs)

        type_hints = get_args(cls.__orig_bases__[0])
        assert len(type_hints) == 4, "CRUDService must have exactly 4 type hints"
        assert issubclass(type_hints[0], EntityObjectBase), "`type_hints[0]` must be a subclass of `EntityObjectBase`"
        assert issubclass(type_hints[1], ObjectBase), "`type_hints[1]` must be a subclass of `ObjectBase`"
        assert issubclass(type_hints[2], ObjectBase), "`type_hints[2]` must be a subclass of `ObjectBase`"
        assert issubclass(type_hints[3], EntityMapperBase), "`type_hints[3]` must be a subclass of `EntityMapperBase`"

        cls.EntityType = type_hints[0]
        cls.CreateType = type_hints[1]
        cls.UpdateType = type_hints[2]
        cls.MapperType = type_hints[3]

    # Constructor
    # -----------

    def __init__(self, db: Annotated[DBSession, Depends(new_db_session)]) -> None:
        self.db = db

    # Private methods
    # ---------------

    @abstractmethod
    def _get_optional_row(self, *, id: IdField) -> Optional[_TMapperType]:
        return self.db.exec(select(self.MapperType).where(column(self.MapperType.id) == id)).first()

    @abstractmethod
    def _get_row_or_raise(self, *, id: IdField) -> _TMapperType:
        row = self._get_optional_row(id=id)
        if row is None:
            raise NotFoundHTTPException(self.EntityType, f" with id = {id}")
        return row

    @abstractmethod
    def _construct_entity(self, row: _TMapperType) -> _TEntityType:
        return self.EntityType.model_validate(row)

    # Public methods
    # --------------

    @abstractmethod
    def get(self, *, id: IdField) -> _TEntityType:
        # Get the row from the database by ID
        row = self._get_row_or_raise(id=id)
        return self._construct_entity(row)

    @abstractmethod
    def get_list(self, *, offset: Optional[int] = None, limit: Optional[int] = None) -> List[_TEntityType]:
        # Prepare the select statement and apply the offset and limit
        stmt = select(self.MapperType)
        if offset is not None:
            stmt = stmt.offset(max(0, offset))
        if limit is not None:
            stmt = stmt.limit(max(0, min(limit, API_RESOURCE_QUERY_PAGE_MAX)))

        # Execute the statement to get the rows
        rows = self.db.exec(stmt).all()

        # Return a list of entities constructed from the rows
        return [self._construct_entity(row) for row in rows]

    @abstractmethod
    def create(self, *, data: _TCreateType) -> _TEntityType:
        # Create a new row object and commit it to the database
        row = self.MapperType.model_validate(data)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)

        # Return the new entity constructed from the row
        return self._construct_entity(row)

    @abstractmethod
    def update(self, *, id: IdField, data: _TUpdateType) -> _TEntityType:
        # Get the row from the database
        row = self._get_row_or_raise(id=id)

        # Update the entity with the new values and set the `updated_at` field
        row = row.model_copy(update=data.model_dump(exclude_unset=True))
        row.updated_at = datetime.now()

        # Commit the changes to the database
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)

        # Return the entity updated with the new values
        return self._construct_entity(row)

    @abstractmethod
    def delete(self, id: IdField) -> _TEntityType:
        # Get the row from the database
        row = self._get_row_or_raise(id=id)

        # Delete the row from the database
        self.db.delete(row)
        self.db.commit()

        # Return the entity constructed from the deleted row
        return self._construct_entity(row)
