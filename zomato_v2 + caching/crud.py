from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from models import Restaurant
from schemas import RestaurantCreate, RestaurantUpdate

async def create_restaurant(
    db: AsyncSession, payload: RestaurantCreate
) -> Restaurant:
    obj = Restaurant(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_restaurants(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> List[Restaurant]:
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    return result.scalars().all()

async def get_restaurant(
    db: AsyncSession, restaurant_id: int
) -> Optional[Restaurant]:
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    return result.scalar_one_or_none()

async def update_restaurant(
    db: AsyncSession,
    restaurant_id: int,
    payload: RestaurantUpdate
) -> Optional[Restaurant]:
    stmt = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    obj = stmt.scalar_one_or_none()
    if not obj:
        return None
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj

async def delete_restaurant(
    db: AsyncSession, restaurant_id: int
) -> Optional[Restaurant]:
    stmt = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    obj = stmt.scalar_one_or_none()
    if not obj:
        return None
    await db.delete(obj)
    await db.commit()
    return obj

async def search_restaurants_by_cuisine(
    db: AsyncSession,
    cuisine: str,
    skip: int = 0,
    limit: int = 100
) -> List[Restaurant]:
    stmt = select(Restaurant).where(
        Restaurant.cuisine_type.ilike(f"%{cuisine}%")
    ).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_active_restaurants(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[Restaurant]:
    stmt = select(Restaurant).where(Restaurant.is_active).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
