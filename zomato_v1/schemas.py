from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time

class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: str = Field(..., min_length=2, max_length=50)
    address: str = Field(..., min_length=5, max_length=200)
    phone_number: str = Field(
        ...,
        pattern=r"^\+?[0-9\- ]{7,20}$",
        description="Phone number with country code, digits, dashes or spaces"
    )
    rating: float = Field(0.0, ge=0.0, le=5.0)
    is_active: bool = True
    opening_time: time
    closing_time: time

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: Optional[str] = Field(None, min_length=2, max_length=50)
    address: Optional[str] = Field(None, min_length=5, max_length=200)
    phone_number: Optional[str] = Field(
        None,
        pattern=r"^\+?[0-9\- ]{7,20}$",
        description="Phone number with country code, digits, dashes or spaces"
    )
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    is_active: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

class RestaurantResponse(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
