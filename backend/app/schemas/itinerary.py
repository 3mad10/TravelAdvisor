from pydantic import BaseModel, ValidationInfo, field_validator
from pydantic import Field as PydanticField
from datetime import date, datetime
from sqlmodel import Field, Relationship, SQLModel
from schemas.user import User
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Annotated, List

if TYPE_CHECKING:
    from schemas.itinerary import UserItinerary


class ItinraryActivityLink(SQLModel, table=True):
    itinerary_id: UUID = Field(foreign_key="itinerary.id", primary_key=True)
    activity_id: int = Field(foreign_key="activity.id", primary_key=True)
    day: int = Field(ge=1)


class ActivityBase(BaseModel):
    short_name: str
    location: str
    full_description: str | None = PydanticField(default=None, description="Full description for the activity")
    img_url: str | None = PydanticField(default=None, description="Full description for the activity")


class ActivityLLMOutput(ActivityBase):
    day: int = PydanticField(default=None, ge=1, description="Full description for the activity")

class ActivityWithId(ActivityLLMOutput):
    id: int

# Activity table
class Activity(ActivityBase, SQLModel, table=True):
    id: int = Field(primary_key=True)
    Itineraries: List["Itinerary"] = Relationship(back_populates="activities", link_model=ItinraryActivityLink)


class ItineraryBase(BaseModel):
    destination: str = PydanticField(description="Destination either Country or City")
    interests: list[str] = PydanticField(description="List of User interests in this Itinirary")
    rating: float | None = PydanticField(default=None, ge=0, le=5, description="Rating of the Itinerary")


# Public Itinerary Table
class Itinerary(ItineraryBase, SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    interests: str = Field(description="String of User interests in this Itinirary seperated by comma")
    activities: List["Activity"] = Relationship(back_populates="Itineraries", link_model=ItinraryActivityLink)
    users_itineraries: List["UserItinerary"] = Relationship(back_populates="itinerary")

class ItineraryOutput(ItineraryBase):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    interests: str = PydanticField(description="String of User interests in this Itinirary seperated by comma")
    activities: List[ActivityLLMOutput]

# Private Itinerary Schemas
class UserItineraryLLMInput(ItineraryBase):
    start_date: date
    end_date: date
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "destination": "paris",
                    "interests": [
                        "sightseeing"
                    ],
                    "rating": None,
                    "start_date": "2026-08-03",
                    "end_date": "2026-08-06"
                }
            ]
        }
    }

class UserItineraryCreate(ItineraryBase):
    start_date: date
    end_date: date
    activities: list[ActivityLLMOutput]
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
                    "end_date": "2026-08-08",
                    "activities": [
                            {
                                "day": 1,
                                "short_name": "Skying on Mount Everest",
                                "location": "Mount Everest"
                            },
                        ],
                }
            ]
        }
    }


class UserItineraryUpdate(BaseModel):
    start_date: date | None
    end_date: date | None
    destination: str | None = PydanticField(description="Destination either Country or City")
    interests: list[str] | None = PydanticField(description="List of User interests in this Itinirary")
    activities: list[ActivityWithId] | None
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
                    "end_date": "2026-08-08",
                    "activities": [
                            {
                                "id": 5,
                                "short_name": "Skying on Mount Everest",
                                "location": "Mount Everest"
                            },
                            {
                                "id": 6,
                                "short_name": "Eat chocolate",
                                "location": "Wherever"
                            }
                        ]
                    }
            ]
        }
    }


# Private Itinerary Table
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

class UserItineraryUpdated(ItineraryOutput):
    start_date: date
    end_date: date