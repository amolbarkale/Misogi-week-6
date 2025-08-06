from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from schemas import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantResponse
)
import crud

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"]
)

@router.post(
    "/",
    response_model=RestaurantResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_restaurant(
    restaurant: RestaurantCreate,
    db: AsyncSession = Depends(get_db)
):
    # Prevent duplicate names
    existing = await crud.search_restaurants_by_cuisine(
        db, cuisine=restaurant.name, skip=0, limit=1
    )
    if any(r.name == restaurant.name for r in existing):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Restaurant with this name already exists."
        )
    return await crud.create_restaurant(db, restaurant)

@router.get(
    "/",
    response_model=List[RestaurantResponse]
)
async def read_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_restaurants(db, skip=skip, limit=limit)

@router.get(
    "/{restaurant_id}",
    response_model=RestaurantResponse
)
async def read_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_restaurant = await crud.get_restaurant(db, restaurant_id)
    if not db_restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found."
        )
    return db_restaurant

@router.put(
    "/{restaurant_id}",
    response_model=RestaurantResponse
)
async def update_restaurant(
    restaurant_id: int,
    restaurant: RestaurantUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await crud.update_restaurant(db, restaurant_id, restaurant)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found."
        )
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found."
        )
    return deleted

@router.get(
    "/search",
    response_model=List[RestaurantResponse]
)
async def search_by_cuisine(
    cuisine: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.search_restaurants_by_cuisine(
        db, cuisine=cuisine, skip=skip, limit=limit
    )

@router.get(
    "/active",
    response_model=List[RestaurantResponse]
)
async def list_active_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_active_restaurants(db, skip=skip, limit=limit)
