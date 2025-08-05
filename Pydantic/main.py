from pydantic import BaseModel , Field, field_validator, ValidationError
from typing import Optional

class PydanticUser(BaseModel):
    name: str # Automatically validates as a string
    age: int # Automatically validates as a string

pydantic = PydanticUser(name="amol", age= 32)

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, description="Price must be positive")
    quantity: int = Field(default=0, ge=0)

product = Product(name="amol", price=120, quantity=3)
# print('product:', product)
#___________________________________________________________
# Validators
class User(BaseModel):
    email: str

    @field_validator("email")
    def email_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")

user = User(email="amol@gmail.com")
#___________________________________________________________

# def register(data):
#     user = {
#         "name": data["age"],
#         "email": data["age"],
#         "age":data["age"]
#     }
#     return user

# user_values = {
#     "name": "John",
#     "email": "not an email",
#     "age": "twenty-five"
# }

# register(user_values)

class User(BaseModel):
    name: str
    email: str
    age: int

def register_user(data):
    try:
        user = User(**data)
        print('user is validated:', user)
        return user
    except ValidationError as e:
        print(f"Incorrect input feed: {e}")
        return None

# valid_data = {"name": "John", "email": "john@example.com", "age": 25}
# result = register_user(valid_data)

# invalid_data = {"name": "John", "age": "25"}
# result = register_user(invalid_data)
#___________________________________________________________


class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    description: Optional[str] = None

product1_data = {
    "id": 123,
    "name": "amol",
    "price": 123.45,
    "in_stock": True,
    "description": "High performajsdng "
}

# product2_data = {
#     "id": "123", # string that can become int
#     "name": "amol",
#     "price": "123.45", # string that can become float
#     "in_stock": "true",
#     "description": "High performajsdng "
# }

product2 = Product(**product1_data)
# print('product2:', product2)
#___________________________________________________________

# Async await

# import asyncio
# import time


