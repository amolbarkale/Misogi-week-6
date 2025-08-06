from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time
from decimal import Decimal

# ─────────── Restaurant Schemas (Version 1) ───────────

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
    """All fields required to create a restaurant."""
    pass

class RestaurantUpdate(BaseModel):
    """All fields optional for updating a restaurant."""
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
    """Response model returned to clients for restaurants."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ─────────── MenuItem Schemas (Version 2) ───────────

class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(
        ...,
        gt=0,
        description="Positive price, two decimal places"
    )
    category: str = Field(..., min_length=2, max_length=50)
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_available: bool = True
    preparation_time: int = Field(
        ...,
        gt=0,
        description="Preparation time in minutes"
    )

class MenuItemCreate(MenuItemBase):
    """All fields required to create a menu item."""
    pass

class MenuItemUpdate(BaseModel):
    """All fields optional for updating a menu item."""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = Field(None, gt=0)

class MenuItemResponse(MenuItemBase):
    """Response model returned to clients for menu items."""
    id: int
    restaurant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ─────────── Nested / Combined Schemas ───────────

class RestaurantWithMenu(RestaurantResponse):
    """Restaurant plus its menu items."""
    menu_items: List[MenuItemResponse]

    class Config:
        from_attributes = True

class MenuItemWithRestaurant(MenuItemResponse):
    """Menu item plus its parent restaurant details."""
    restaurant: RestaurantResponse

    class Config:
        from_attributes = True
