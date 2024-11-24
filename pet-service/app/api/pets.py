from typing import List
from fastapi import APIRouter, HTTPException, Response, Depends

from app.api.models import (
    PetOut,
    PetIn,
    Link,
    PetListResponse,
    PetFilterParams,
    PetUpdate,
)
from app.api import db_manager
import uuid
import os

# from app.api.service import is_cast_present

pets = APIRouter()
URL_PREFIX = os.getenv("URL_PREFIX")


@pets.post("/", response_model=PetOut, status_code=201)
async def create_pet(payload: PetIn, response: Response):
    # for cast_id in payload.casts_id:
    #     if not is_cast_present(cast_id):
    #         raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    pet_id = str(uuid.uuid4())
    await db_manager.add_pet(payload, pet_id=pet_id)

    pet_url = generate_pet_url(pet_id=pet_id)
    response.headers["Location"] = pet_url

    response.headers["Link"] = f'<{pet_url}>; rel="self", </pets/>; rel="collection"'

    response_data = PetOut(
        id=pet_id,
        name=payload.name,
        type=payload.type,
        price=payload.price,
        breeder_id=payload.breeder_id,
        image_url=payload.image_url,  # Include image_url
        links=[
            Link(rel="self", href=pet_url),
            Link(rel="collection", href=f"{URL_PREFIX}/pets/"),
        ],
    )
    return response_data


@pets.get("/", response_model=PetListResponse)
async def get_pets(params: PetFilterParams = Depends()):
    db_records = await db_manager.get_all_pets(
        limit=params.limit, offset=params.offset, type=params.type
    )

    pets = [
        PetOut(
            id=record["id"],
            name=record["name"],
            type=record["type"],
            price=record["price"],
            breeder_id=record["breeder_id"],
            image_url=record["image_url"],  # Include image_url from the database
            links=[
                Link(rel="self", href=f"{URL_PREFIX}/pets/{record['id']}/"),
                Link(rel="collection", href=f"{URL_PREFIX}/pets/"),
            ],
        )
        for record in db_records
    ]

    # Add Link headers to paginate and return a collection link in response
    links = [
        Link(rel="self", href=f"{URL_PREFIX}/pets/"),
        Link(rel="collection", href=f"{URL_PREFIX}/pets/"),
    ]

    if params.limit:
        next_offset = params.offset + params.limit
        links.append(
            Link(rel="next", href=f"{URL_PREFIX}/pets/?limit={params.limit}&offset={next_offset}")
        )

    return PetListResponse(
        data=pets,
        links=links,
    )


@pets.get("/{id}/", response_model=PetOut)
async def get_pet(id: str):
    pet = await db_manager.get_pet(id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    # Include link to self and collection in the response
    response_data = PetOut(
        id=pet["id"],
        name=pet["name"],
        type=pet["type"],
        price=pet["price"],
        breeder_id=pet["breeder_id"],
        image_url=pet["image_url"],  # Include image_url from the database
        links=[
            Link(rel="self", href=f"{URL_PREFIX}/pets/{id}/"),
            Link(rel="collection", href=f"{URL_PREFIX}/pets/"),
        ],
    )
    return response_data


@pets.put("/{id}/", response_model=PetOut)
async def update_pet(id: str, payload: PetUpdate):
    pet = await db_manager.get_pet(id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    update_data = payload.model_dump(exclude_unset=True)
    pet_in_db = PetIn(**pet)
    updated_pet = pet_in_db.model_copy(update=update_data)

    await db_manager.update_pet(id, updated_pet)
    updated_pet_in_db = await db_manager.get_pet(id)

    # Include updated response with link sections
    response_data = PetOut(
        id=updated_pet_in_db["id"],
        name=updated_pet_in_db["name"],
        type=updated_pet_in_db["type"],
        price=updated_pet_in_db["price"],
        breeder_id=updated_pet_in_db["breeder_id"],
        image_url=updated_pet_in_db["image_url"],  # Include image_url
        links=[
            Link(rel="self", href=f"{URL_PREFIX}/pets/{id}/"),
            Link(rel="collection", href=f"{URL_PREFIX}/pets/"),
        ],
    )
    return response_data


@pets.delete("/{id}/", response_model=None, status_code=200)
async def delete_pets(id: str):
    pet = await db_manager.get_pet(id)
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return await db_manager.delete_pet(id)


@pets.delete("/delete/all/", response_model=None, status_code=200)
async def delete_all_pets():
    try:
        await db_manager.delete_all_pets()
        return {"message": "All pets have been deleted."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete all pets: {str(e)}"
        )

# get pets by breeder_id
@pets.get("/breeder/{breeder_id}/", response_model=List[PetOut])
async def get_pets_by_breeder(breeder_id: str):
    pets = await db_manager.get_pets_by_breeder(breeder_id)
    if not pets:
        return []

    # Include links for each pet in the response
    response_data = [
        PetOut(
            id=pet["id"],
            name=pet["name"],
            type=pet["type"],
            price=pet["price"],
            breeder_id=pet["breeder_id"],
            image_url=pet["image_url"],  # Include image_url from the database
        )
        for pet in pets
    ]
    return response_data

#### Helper functions

def generate_pet_url(pet_id: str):
    return f"{URL_PREFIX}/pets/{pet_id}/"
