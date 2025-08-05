from fastapi import FastAPI, HTTPException, Depends, status
from enum import Enum
from decimal import Decimal

from pydantic import BaseModel, field_validator, ValidationError, Field, condecimal, conint, conlist
from typing import Optional, Dict, List

# 1. Category enum
class FoodCategory(str, Enum):
    APPETIZER   = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT     = "dessert"
    BEVERAGE    = "beverage"
    SALAD       = "salad"

class FoodItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100,
                      description="Name of the item (3–100 chars)")
    description: str = Field(..., min_length=10, max_length=500,
                             description="Description (10–500 chars)")
    category: FoodCategory
    price: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(
        ..., description="Positive, up to 2 decimal places"
    )
    is_available: bool = Field(True, description="Is it on the menu?")
    preparation_time: conint(ge=1, le=120) = Field(
        ..., description="Minutes (1–120)"
    )
    ingredients: conlist(str, min_items=1) = Field(
        ..., description="At least one ingredient"
    )
    calories: Optional[conint(gt=0)] = Field(
        None, description="Optional positive calorie count"
    )
    is_vegetarian: bool = Field(False, description="Vegetarian?")
    is_spicy: bool = Field(False, description="Spicy?")

# 3. Full model including auto‐generated ID
class FoodItem(FoodItemBase):
    id: int = Field(..., description="Auto‐generated unique ID")


menu_db = Dict[int, "FoodItem"] = {}
next_id: int = 1

# ─── App & Auth Stub ───────────────────────────────────────────────────────────

app = FastAPI()

def get_current_staff_user():
    """
    Stub for “staff only” dependency.
    Replace this with real auth (JWT/session) in production.
    """
    is_staff = True
    if not is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized")
    return True

# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/menu", response_model=List[FoodItem])
def get_all_menu_items():
    return list(menu_db.values())

@app.get("/menu/{item_id}", response_model=FoodItem)
def get_menu_item(item_id: int):
    item = menu_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post(
    "/menu",
    response_model=FoodItem,
    status_code=status.HTTP_201_CREATED,
)
def create_menu_item(
    item: FoodItemBase,
    staff: bool = Depends(get_current_staff_user),
):
    global next_id
    new_item = FoodItem(id=next_id, **item.dict())
    menu_db[next_id] = new_item
    next_id += 1
    return new_item

@app.put("/menu/{item_id}", response_model=FoodItem)
def update_menu_item(
    item_id: int,
    item: FoodItemBase,
    staff: bool = Depends(get_current_staff_user),
):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = FoodItem(id=item_id, **item.dict())
    menu_db[item_id] = updated
    return updated

@app.delete(
    "/menu/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_menu_item(
    item_id: int,
    staff: bool = Depends(get_current_staff_user),
):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del menu_db[item_id]
    return

@app.get("/menu/category/{category}", response_model=List[FoodItem])
def get_items_by_category(category: FoodCategory):
    return [item for item in menu_db.values() if item.category == category]