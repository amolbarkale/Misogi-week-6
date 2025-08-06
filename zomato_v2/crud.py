# crud.py (add after existing Restaurant CRUD)

from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from models import MenuItem, Restaurant
from schemas import MenuItemCreate, MenuItemUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from decimal import Decimal

async def create_menu_item(
    db: AsyncSession,
    restaurant_id: int,
    item: MenuItemCreate
) -> MenuItem:
    # 1) Ensure parent restaurant exists
    res = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    parent = res.scalar_one_or_none()
    if not parent:
        return None

    # 2) Build & save the new MenuItem
    db_item = MenuItem(**item.dict(), restaurant_id=restaurant_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_menu_item(
    db: AsyncSession,
    item_id: int
) -> Optional[MenuItem]:
    result = await db.execute(
        select(MenuItem).where(MenuItem.id == item_id)
    )
    return result.scalar_one_or_none()

async def get_all_menu_items(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[MenuItem]:
    result = await db.execute(
        select(MenuItem).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_menu_item(
    db: AsyncSession,
    item_id: int,
    item_update: MenuItemUpdate
) -> Optional[MenuItem]:
    # Fetch existing
    res = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    db_item = res.scalar_one_or_none()
    if not db_item:
        return None

    # Apply changes
    update_data = item_update.dict(exclude_unset=True)
    for field, val in update_data.items():
        setattr(db_item, field, val)

    await db.commit()
    await db.refresh(db_item)
    return db_item

async def delete_menu_item(
    db: AsyncSession,
    item_id: int
) -> Optional[MenuItem]:
    res = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    db_item = res.scalar_one_or_none()
    if not db_item:
        return None
    await db.delete(db_item)
    await db.commit()
    return db_item

async def search_menu_items(
    db: AsyncSession,
    category: Optional[str] = None,
    vegetarian: Optional[bool] = None,
    vegan: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> List[MenuItem]:
    # Build base query
    stmt = select(MenuItem)
    if category:
        stmt = stmt.where(MenuItem.category.ilike(f"%{category}%"))
    if vegetarian is not None:
        stmt = stmt.where(MenuItem.is_vegetarian == vegetarian)
    if vegan is not None:
        stmt = stmt.where(MenuItem.is_vegan == vegan)

    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_menu_for_restaurant(
    db: AsyncSession,
    restaurant_id: int
) -> List[MenuItem]:
    result = await db.execute(
        select(MenuItem)
        .where(MenuItem.restaurant_id == restaurant_id)
    )
    return result.scalars().all()

async def get_restaurant_with_menu(
    db: AsyncSession,
    restaurant_id: int
) -> Optional[Restaurant]:
    # Use selectinload to pull in menu_items efficiently
    result = await db.execute(
        select(Restaurant)
        .options(selectinload(Restaurant.menu_items))
        .where(Restaurant.id == restaurant_id)
    )
    return result.scalar_one_or_none()
