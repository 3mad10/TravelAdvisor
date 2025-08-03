from pydantic import BaseModel, ValidationInfo, field_validator
from datetime import date, datetime
from sqlmodel import Field, Relationship, SQLModel
from schemas.user import User
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Annotated, List

if TYPE_CHECKING:
    from schemas.itinerary import UserItinerary


class ActivityBase(SQLModel):
    location: str
    description: str | None
    img_url: str | None


class Activity(ActivityBase, table=True):
    id: int = Field(primary_key=True)


class ItineraryInput(BaseModel):
    destination: str = Field(description="Destination either Country or City")
    interests: str


class ItineraryBase(ItineraryInput, SQLModel):
    rating: float | None = Field(ge=0, le=5, description="Rating of the Itinerary")

class Itinerary(ItineraryBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    users_itineraries: List["UserItinerary"] = Relationship(back_populates="itinerary")

class UserItineraryInput(ItineraryInput):
    start_date: date
    end_date: date

class UserItineraryInputValidate(BaseModel):
    start_date: date
    end_date: date
    destination: str = Field(description="Destination either Country or City")
    interests: list[str]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "destination": "switzerland",
                    "interests": [
                        "nature",
                        "food"
                    ],
                    "start_date": "2026-08-03",
                    "end_date": "2026-08-08"
                }
            ]
        }
    }

class ItineraryCreate(ItineraryBase):
    activities: list[ActivityBase]

class UserItineraryCreate(UserItineraryInput, SQLModel):
    activities: list[ActivityBase]

class UserItinerary(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    start_date: date
    end_date: date
    itinerary_id: Annotated[UUID, Field(foreign_key="itinerary.id")]
    user_id: Annotated[UUID, Field(foreign_key="user.id")]
    itinerary: Itinerary = Relationship(back_populates="users_itineraries")
    user: User = Relationship(back_populates="itineraries")

    @field_validator('end_date')
    def check_start_and_end_date(cls, value: date, info: ValidationInfo):
        if info.data['start_date'] >= value:
            raise ValueError("End date must be after start date")
        return value

class ItinraryActivityLink(SQLModel, table=True):
    itinerary_id: UUID = Field(foreign_key="itinerary.id", primary_key=True)
    activity_id: int = Field(foreign_key="activity.id", primary_key=True)
    day: int = Field(ge=1)

