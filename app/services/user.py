from fastapi import Depends, HTTPException, status as http_status
from passlib.context import CryptContext
from typing_extensions import Optional

from app.schemas.user import User, UserCreate, UserUpdate, UserPasswordUpdate
from app.services.error import NotFoundHTTPException
from app.storage.mappers import UserMapper, select, column
from app.services.mixins import EntityCRUDMixin
from app.utilities import overrides


class UserService(EntityCRUDMixin[User, UserCreate, UserUpdate, UserMapper]):
    _pwd_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Class methods
    # -------------

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls._pwd_hasher.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls._pwd_hasher.verify(password, hashed_password)

    # Private methods
    # ---------------

    def _get_optional_row_by_email(self, email: str) -> Optional[UserMapper]:
        stmt = select(UserMapper).where(column(UserMapper.email) == email)
        return self.db.exec(stmt).first()

    def _get_row_by_email_or_raise(self, email: str) -> UserMapper:
        row = self._get_optional_row_by_email(email)
        if row is None:
            raise NotFoundHTTPException(User, f" with email = {email}")
        return row

    # Public methods
    # --------------

    def get_by_email(self, email: str) -> User:
        row = self._get_row_by_email_or_raise(email)
        return self._construct_entity(row)

    def authenticate_and_get_user(self, *, email: str, password: str) -> User:
        row = self._get_row_by_email_or_raise(email)
        if not self.verify_password(password, row.hashed_password):
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
            )
        return self._construct_entity(row)

    @overrides(EntityCRUDMixin)
    def create(self, *, data: UserCreate) -> User:
        row = self._get_optional_row_by_email(data.email)
        if row is not None:
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail="User already exists",
            )
        
        row = UserMapper(
            **data,
            hashed_password=self.__class__.hash_password(data.password),
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        
        return self._construct_entity(row)

    def update_password(self, *, email: str, data: UserPasswordUpdate) -> User:
        row = self._get_row_by_email_or_raise(email)
        if not self.verify_password(data.old_password, row.hashed_password):
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
            )

        row.hashed_password = self.hash_password(data.new_password)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)

        return self._construct_entity(row)
