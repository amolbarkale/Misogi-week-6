from pydantic import BaseModel
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    price: float
    genre: str

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None
    genre: Optional[str] = None

class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
