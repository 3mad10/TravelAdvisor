from fastapi import APIRouter, HTTPException, Query, Path, status
from core.config import settings
from uuid import uuid4, UUID
from core.crud import get_user_by_id, get_itinerary_by_id
from schemas.itinerary import (
    Activity,
    ActivityLLMOutput,
    ActivityWithId,
    Itinerary,
    ItineraryOutput,
    ItinraryActivityLink,
    UserItinerary,
    UserItineraryCreate,
    UserItineraryLLMInput,
    UserItineraryUpdate,
)
from sqlmodel import func, select, delete
from sqlalchemy.orm import selectinload
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

@router.post("/generate", response_model=list[ActivityLLMOutput])
async def generate_route(*, info: UserItineraryLLMInput):
    prompt = f"As a professional travel advisor generate an itinerary for a person going to {info.destination} \
        the journey start date is on {info.start_date} and the end date is on {info.end_date} \
        the person interests are {",".join(info.interests)}, if the response activity is large \
        make a short descripion of it then add colons : and add the details after, Don't add dates in the response \
        only Day 1 , Day 2... etc, Return the list of activities, each with: \
        - location name \
        - short description \
        - a valid image URL that ends in .jpg or .png (not a website or placeholder or https://example.com)."
    print(info)
    # TODO Make the image generation using unsplash
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=list[ActivityLLMOutput]
            )
        )
    raw_text = response.candidates[0].content.parts[0].text
    parsed = json.loads(raw_text)
    return [ActivityLLMOutput(**item) for item in parsed]


@router.post("/", response_model=UserItinerary)
async def save_itinerary(*,itinerary_in: UserItineraryCreate,
                         current_user: CurrentUser,
                         session: SessionDep):

    puplic_itinerary_db = Itinerary(
        destination=itinerary_in.destination,
        interests=",".join(itinerary_in.interests),
        rating=None)
    
    session.add(puplic_itinerary_db)
    session.flush()

    for activity_input in itinerary_in.activities:
        activity = Activity(
            short_name=activity_input.short_name,
            location=activity_input.location,
            full_description=activity_input.full_description,
            img_url=activity_input.img_url
        )
        session.add(activity)
        session.flush()

        # Link the activity with the itinerary using the day field
        link = ItinraryActivityLink(
            itinerary_id=puplic_itinerary_db.id,
            activity_id=activity.id,
            day=activity_input.day
        )
        session.add(link)

    private_itinerary_db = UserItinerary(
        start_date=itinerary_in.start_date,
        end_date=itinerary_in.end_date,
        user_id=current_user.id,
        itinerary=puplic_itinerary_db
    )
    user_db = get_user_by_id(session=session, user_id=current_user.id)
    private_itinerary_db.itinerary = puplic_itinerary_db
    session.add(private_itinerary_db)
    session.commit()
    session.refresh(puplic_itinerary_db)
    session.refresh(private_itinerary_db)
    session.refresh(user_db)
    return private_itinerary_db


@router.delete("/{id}", response_model=UserItinerary)
async def delete_itinerary(*, id: Annotated[UUID, Path(title="The ID of the itinerary to delete")],
                           current_user: CurrentUser,
                           session: SessionDep):
    user_db = get_user_by_id(session=session, user_id=current_user.id)
    itinerary_db = get_itinerary_by_id(session=session, itinerary_id=id)
    if itinerary_db in user_db.itineraries:
        session.delete(itinerary_db)
        session.commit()
        return itinerary_db
    else:
        raise HTTPException(
                status_code=401, detail="Unauthorized"
            )


@router.get("/", response_model=list[UserItinerary])
async def get_user_itineraries(*, current_user: CurrentUser,
                               session: SessionDep):
    user_db = get_user_by_id(session=session, user_id=current_user.id)
    print("user_db : ")
    print(user_db)
    if user_db:
        user_itineraries = session.exec(
            select(UserItinerary).where(UserItinerary.user_id == current_user.id)
        )
        print("user_itineraries  : ", user_itineraries)
        return user_itineraries
    else:
        raise HTTPException(
                status_code=401, detail="Unauthorized"
            )


@router.get("/{public_itinerary_id}", response_model=ItineraryOutput)
async def get_public_itinerary(*, public_itinerary_id: UUID, session: SessionDep):
    itinerary = session.exec(
        select(Itinerary).where(Itinerary.id == public_itinerary_id)
    ).first()
    if not itinerary:
        raise HTTPException(
                status_code=404, detail="Itinerary not found"
            )
    else:
        # Join link table with Activity to get the day field
        results = session.exec(
            select(ItinraryActivityLink, Activity)
            .join(Activity, Activity.id == ItinraryActivityLink.activity_id)
            .where(ItinraryActivityLink.itinerary_id == public_itinerary_id)
        ).all()

        activities = [
            ActivityWithId(
                short_name=activity.short_name,
                location=activity.location,
                full_description=activity.full_description,
                img_url=activity.img_url,
                day=link.day,
                id=activity.id
            )
            for link, activity in results
        ]

        return ItineraryOutput(
            id=itinerary.id,
            interests=itinerary.interests,
            destination=itinerary.destination,
            rating=itinerary.rating,
            activities=activities
        )


@router.patch("/{private_itinerary_id}", response_model=UserItinerary)
async def update_private_itinerary(*, updated_itinirary: UserItineraryUpdate,
                                   private_itinerary_id: UUID,
                                   session: SessionDep,
                                   current_user: CurrentUser):
    user_db = get_user_by_id(session=session, user_id=current_user.id)
    private_itinerary_db = get_itinerary_by_id(session=session, itinerary_id=private_itinerary_id)
    print("user_db : ")
    print(user_db)
    print("private_itinerary_db : ")
    print(private_itinerary_db) 
    if not private_itinerary_db:
        raise HTTPException(
                status_code=404, detail="User Itinerary not found"
            )
    public_itinerary_db = session.exec(
        select(Itinerary).where(Itinerary.id == private_itinerary_db.itinerary_id)
    ).first()
    if not public_itinerary_db:
        raise HTTPException(
                status_code=404, detail="Associated Itinerary not found"
            )
    # TODO if the itinerary is assigned by multiple users (check users > 1) create new publi itinerary
    # add it to database and update the user private itinerary with the new one
    updated_itinerary = updated_itinirary.model_dump(exclude_unset=True)
    public_itinerary_db.sqlmodel_update(updated_itinerary)
    private_itinerary_db.itinerary = public_itinerary_db
    # TODO Handle deleting and adding new activities
    if updated_itinerary["activities"]:
        for updated_activity in updated_itinerary["activities"]:
            activity_db = session.exec(
                select(Activity).where(Activity.id == updated_activity["id"])
            ).first()

            if not activity_db:
                raise HTTPException(
                    status_code=404, detail="updated activity not found"
                )
            link = session.exec(
                    select(ItinraryActivityLink)
                    .where(ItinraryActivityLink.activity_id == activity_db.id)
                    .where(ItinraryActivityLink.itinerary_id == public_itinerary_db.id)
                ).first()

            if not link:
                raise HTTPException(
                    status_code=404, detail="Activity not part of the current itinerary"
                )
            if "day" in updated_activity:
                link.day = updated_activity["day"]
                session.add(link)
            
            activity_db.sqlmodel_update(updated_activity)
            session.add(activity_db)
            session.commit()
            
    session.add(public_itinerary_db)
    session.add(private_itinerary_db)
    session.commit()
    session.refresh(public_itinerary_db)
    session.refresh(private_itinerary_db)
    return private_itinerary_db
