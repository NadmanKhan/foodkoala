from pydantic import EmailStr, SecretStr
from typing_extensions import Annotated, List, Optional

from app.schemas.bases import EntityObjectBase, ObjectBase, Field
from app.schemas.order import Order


EmailField = EmailStr
NameField = Annotated[str, Field(min_length=2, max_length=100)]
PhoneField = Annotated[str, Field(min_length=10, max_length=17, pattern=r"^(?:\+880? ?|0)?(1[3-9]\d{2}-?\d{6})$")]
PasswordField = Annotated[SecretStr, Field(min_length=8, max_length=100)]


class UserBase(ObjectBase):
    email: EmailField
    phone: PhoneField
    name: Optional[NameField] = None


class UserCreate(UserBase):
    password: PasswordField


class UserUpdate(UserBase):
    email: EmailField = None
    phone: PhoneField = None
    name: NameField = None

class UserPasswordUpdate(ObjectBase):
    old_password: PasswordField
    new_password: PasswordField


class User(UserBase, EntityObjectBase):
    orders: List[Order] = []