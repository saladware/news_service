from datetime import date
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class Gender(StrEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    fullname: str
    gender: Gender
    birthday: date


class User(BaseModel):
    id: UUID
    email: EmailStr
    fullname: str
    gender: Gender
    birthday: date

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    email: EmailStr | None
    fullname: str | None
    gender: Gender | None
    birthday: date | None


class ChangePassword(BaseModel):
    new_password: str
    old_password: str

