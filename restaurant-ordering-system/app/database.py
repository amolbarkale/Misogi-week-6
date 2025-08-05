from typing import Dict
from app.models import FoodItem, Order

# In-memory stores
menu_db: Dict[int, FoodItem] = {}
orders_db: Dict[int, Order] = {}

# Auto-incrementing IDs
next_menu_id: int = 1
next_order_id: int = 1
