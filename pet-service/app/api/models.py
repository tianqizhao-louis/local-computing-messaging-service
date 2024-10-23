from pydantic import BaseModel
from typing import List, Optional


class Link(BaseModel):
    rel: str
    href: str


class PetIn(BaseModel):
    name: str
    type: str
    price: float
    breeder_id: str


class PetOut(PetIn):
    id: str
    links: Optional[List[Link]] = None


class PetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    price: Optional[float] = None
    breeder_id: Optional[str] = None


class PetFilterParams(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    type: Optional[str] = None


class PetListResponse(BaseModel):
    data: List[PetOut]
    links: Optional[List[Link]] = None
