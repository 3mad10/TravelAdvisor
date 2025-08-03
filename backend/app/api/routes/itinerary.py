from fastapi import APIRouter, HTTPException, Query, Path, status
from core.config import settings
from uuid import uuid4, UUID
from core.crud import get_user_by_id, get_itinerary_by_id
from schemas.itinerary import (
    UserItineraryInput,
    ActivityBase,
    UserItineraryCreate,
    UserItinerary,
    ItineraryCreate,
    UserItineraryInputValidate,
    Itinerary
)
from sqlmodel import func, select
from typing import Annotated
from schemas.user import User
from google import genai
import json
from google.genai import types
from api.deps import (
    CurrentUser,
    SessionDep,
)

router = APIRouter(prefix="/api/itinerary", tags=["route"])

client = genai.Client(api_key=settings.GEMINI_API_KEY)

@router.post("/generate", response_model=list[ActivityBase])
async def generate_route(*, info: UserItineraryInputValidate):
    prompt = f"As a professional travel advisor generate an itinerary for a person going to {info.destination} \
        the journey start date is on {info.start_date} and the end date is on {info.end_date} \
        the person interests are {",".join(info.interests)}, if the response activity is large \
        make a short descripion of it then add colons : and add the details after, Don't add dates in the response \
        only Day 1 , Day 2... etc, Return the list of activities, each with: \
        - location name \
        - short description \
        - a valid image URL that ends in .jpg or .png (not a website or placeholder or https://example.com)."
    # TODO Make the image generation using unsplash
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=list[ActivityBase]
            )
        )
    raw_text = response.candidates[0].content.parts[0].text
    parsed = json.loads(raw_text)
    return [ActivityBase(**item) for item in parsed]


@router.post("/", response_model=UserItinerary)
async def save_itinerary(*,itinerary_in: UserItineraryCreate,
                         current_user: User = CurrentUser,
                         session: SessionDep):
    puplic_itinerary_db = Itinerary(destination = itinerary_in.destination,
                                       interests = itinerary_in.interests,
                                       rating = None, 
                                       activities = [ActivityBase(**act.model_dump()) for act in itinerary_in.activities])
    
    private_itinerary_db = UserItinerary(
        start_date=itinerary_in.start_date,
        end_date=itinerary_in.end_date,
        user_id=current_user.id,
        itinerary=puplic_itinerary_db
    )
    user_db = get_user_by_id(session=session, user_id = current_user.id)
    private_itinerary_db.itinerary = puplic_itinerary_db
    session.add(puplic_itinerary_db)
    session.add(private_itinerary_db)
    session.commit()
    session.commit()
    session.refresh(puplic_itinerary_db)
    session.refresh(private_itinerary_db)
    session.refresh(user_db)
    return private_itinerary_db


@router.delete("/{id}", response_model=UserItinerary)
async def delete_itinerary(*, id:Annotated[UUID, Path(title="The ID of the itinerary to delete")],
                           current_user: User = CurrentUser,
                           session: SessionDep):
    user_db = get_user_by_id(session=session, user_id = current_user.id)
    itinerary_db = get_itinerary_by_id(session=session, itinerary_id = id)
    if itinerary_db in user_db.itineraries:
        session.delete(itinerary_db)
        session.commit()
        return itinerary_db
    else:
        raise HTTPException(
                status_code=401, detail="Unauthorized"
            )


@router.get("/", response_model=list[UserItinerary])
async def get_user_itineraries(*, current_user: User = CurrentUser,
                               session: SessionDep):
    user_db = get_user_by_id(session=session, user_id=current_user.id)
    if user_db:
        user_itineraries = session.exec(
            select(UserItinerary).where(UserItinerary.user_id == current_user.id)
        )
        return user_itineraries
    else:
        raise HTTPException(
                status_code=401, detail="Unauthorized"
            )


@router.get("/{public_itinerary_id}", response_model=Itinerary)
async def get_public_itinerary(*, public_itinerary_id: UUID, session: SessionDep):
    
    itinerary = session.exec(
        select(Itinerary).where(Itinerary.id == public_itinerary_id)
    ).first()
    return itinerary


# @router.patch("/{private_itinerary_id}", response_model=Itinerary)
# async def update_private_itinerary(*, updated_itinirary: ,
#                                    private_itinerary_id: UUID,
#                                    session: SessionDep, current_user: CurrentUser):
    
#     user_db = get_user_by_id(session=session, user_id=current_user.id)
#     private_itinerary_db = get_itinerary_by_id(session=session, itinerary_id=private_itinerary_id)
#     print("user_db : ")
#     print(user_db)
#     print("private_itinerary_db : ")
#     print(private_itinerary_db) 
#     public_itinerary_db = session.exec(
#         select(Itinerary).where(Itinerary.id == private_itinerary_db.itinerary_id)
#     ).first()

#     if len(public_itinerary_db.users_itineraries) > 1:

#     else:

