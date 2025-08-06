from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models import Restaurant
from schemas import RestaurantCreate, RestaurantUpdate
from typing import List, Optional

async def create_restaurant(
    db: AsyncSession,
    restaurant: RestaurantCreate
) -> Restaurant:
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant

async def get_restaurant(
    db: AsyncSession,
    restaurant_id: int
) -> Optional[Restaurant]:
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    return result.scalar_one_or_none()

async def get_restaurants(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[Restaurant]:
    result = await db.execute(
        select(Restaurant).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_restaurant(
    db: AsyncSession,
    restaurant_id: int,
    restaurant_update: RestaurantUpdate
) -> Optional[Restaurant]:
    # 1. Fetch existing
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    db_restaurant = result.scalar_one_or_none()
    if not db_restaurant:
        return None

    # 2. Apply updates
    update_data = restaurant_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_restaurant, field, value)

    # 3. Commit & refresh
    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant

async def delete_restaurant(
    db: AsyncSession,
    restaurant_id: int
) -> Optional[Restaurant]:
    result = await db.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    db_restaurant = result.scalar_one_or_none()
    if not db_restaurant:
        return None

    await db.delete(db_restaurant)
    await db.commit()
    return db_restaurant

async def search_restaurants_by_cuisine(
    db: AsyncSession,
    cuisine: str,
    skip: int = 0,
    limit: int = 100
) -> List[Restaurant]:
    result = await db.execute(
        select(Restaurant)
        .where(Restaurant.cuisine_type.ilike(f"%{cuisine}%"))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_active_restaurants(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[Restaurant]:
    result = await db.execute(
        select(Restaurant)
        .where(Restaurant.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()
