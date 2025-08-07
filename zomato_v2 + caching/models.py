from sqlalchemy import (
    Column, Integer, String, Boolean,
    Float, Time, DateTime, Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String(100), nullable=False, index=True)
    description  = Column(Text, nullable=True)
    cuisine_type = Column(String(50), nullable=False, index=True)
    address      = Column(String(200), nullable=False)
    phone_number = Column(String(20), nullable=False, unique=True)
    rating       = Column(Float, default=0.0)
    is_active    = Column(Boolean, default=True)
    opening_time = Column(Time, nullable=False)
    closing_time = Column(Time, nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
