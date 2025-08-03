from pydantic import BaseModel, EmailStr, Field
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from itinerary import UserItinerary

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    user_name: str | None = Field(unique=True, default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    user_name: str = Field(max_length=255)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "mabdelm3",
                    "password": "xxxxxxxxxxx",
                    "email": "mabdelm3@gmail.com",
                }
            ]
        }
    }


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)
    user_name: str | None = Field(default=None, max_length=255)


class UserUpdateMe(SQLModel):
    user_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    itineraries: list["UserItinerary"] = Relationship(back_populates="user",
                                                      cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: UUID


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None
