# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional

class House(BaseModel):
    id: Optional[int] = None
    title: str
    price: int
    description: str
    image_url: str
    addressable_str: str
    area_m2: float
    status: str
    residential_number: int

class UpdateHouse(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    addressable_str: Optional[str] = None
    area_m2: Optional[float] = None
    status: Optional[str] = None
    residential_number: Optional[int] = None