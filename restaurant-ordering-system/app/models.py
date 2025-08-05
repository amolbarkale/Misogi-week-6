from enum import Enum
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, condecimal, conint, conlist

# ─── Menu Models ───────────────────────────────────────────────────────────────

class FoodCategory(str, Enum):
    APPETIZER   = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT     = "dessert"
    BEVERAGE    = "beverage"
    SALAD       = "salad"

class FoodItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: FoodCategory
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    is_available: bool = True
    preparation_time: conint(ge=1, le=120)
    ingredients: conlist(str, min_items=1)
    calories: Optional[conint(gt=0)] = None
    is_vegetarian: bool = False
    is_spicy: bool = False

class FoodItem(FoodItemBase):
    id: int

# ─── Order Models ──────────────────────────────────────────────────────────────

class OrderStatus(str, Enum):
    PENDING   = "pending"
    CONFIRMED = "confirmed"
    READY     = "ready"
    DELIVERED = "delivered"

class OrderItem(BaseModel):
    menu_item_id: int = Field(..., ge=1)
    menu_item_name: str = Field(..., min_length=1, max_length=100)
    quantity: conint(gt=0, le=10)
    unit_price: condecimal(gt=0, max_digits=8, decimal_places=2)

    @property
    def item_total(self) -> Decimal:
        return self.quantity * self.unit_price

class Customer(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., regex=r"^\d{10}$")
    address: str = Field(..., min_length=5, max_length=200)

class Order(BaseModel):
    id: int
    customer: Customer
    items: List[OrderItem] = Field(..., min_items=1)
    status: OrderStatus = Field(OrderStatus.PENDING)

    @property
    def total_amount(self) -> Decimal:
        return sum(item.item_total for item in self.items)

class OrderSummary(BaseModel):
    id: int
    status: OrderStatus
    total_amount: Decimal

class StatusUpdate(BaseModel):
    status: OrderStatus
