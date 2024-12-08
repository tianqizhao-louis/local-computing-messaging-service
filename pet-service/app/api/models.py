from typing import Optional, List
from pydantic import BaseModel, HttpUrl  # Import HttpUrl for URL validation


class Link(BaseModel):
    rel: str
    href: str


class PetIn(BaseModel):
    id: Optional[str]
    name: str
    type: str
    price: float
    breeder_id: str
    image_url: Optional[str] = None  # Add image_url as an optional field


class PetOut(PetIn):
    id: str
    links: Optional[List[Link]] = None


class PetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    price: Optional[float] = None
    breeder_id: Optional[str] = None
    image_url: Optional[HttpUrl] = None  # Allow updating the image_url


class PetFilterParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    type: Optional[str] = None


class PetListResponse(BaseModel):
    data: List[PetOut]
    links: Optional[List[Link]] = None
