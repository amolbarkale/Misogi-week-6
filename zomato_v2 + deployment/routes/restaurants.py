from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from schemas import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse,
    RestaurantWithMenu,
    MenuItemCreate,
    MenuItemResponse
)
import crud

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_restaurant(
    payload: RestaurantCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.create_restaurant(db, payload)

@router.get(
    "/",
    response_model=List[RestaurantResponse]
)
async def read_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_restaurants(db, skip, limit)

@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse
)
async def read_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    restaurant = await crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.put(
    "/{restaurant_id}",
    response_model=RestaurantResponse
)
async def update_restaurant(
    restaurant_id: int,
    payload: RestaurantUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await crud.update_restaurant(db, restaurant_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return updated

@router.delete(
    "/{restaurant_id}",
    response_model=RestaurantResponse
)
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_restaurant(db, restaurant_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return deleted

# ─── Menu‐item nested endpoints ─────────────────────────────────

@router.post(
    "/{restaurant_id}/menu-items/",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_menu_item_for_restaurant(
    restaurant_id: int,
    payload: MenuItemCreate,
    db: AsyncSession = Depends(get_db)
):
    item = await crud.create_menu_item(db, restaurant_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Parent restaurant not found")
    return item

@router.get(
    "/{restaurant_id}/menu",
    response_model=List[MenuItemResponse]
)
async def read_menu_for_restaurant(
    restaurant_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_menu_for_restaurant(db, restaurant_id)

@router.get(
    "/{restaurant_id}/with-menu",
    response_model=RestaurantWithMenu
)
async def read_restaurant_with_menu(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    restaurant = await crud.get_restaurant_with_menu(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant
