from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import time

from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache

import crud
from database import get_db
from schemas import (
    RestaurantCreate, RestaurantUpdate, RestaurantResponse
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=RestaurantResponse, status_code=201)
async def create_restaurant(
    payload: RestaurantCreate,
    db: AsyncSession = Depends(get_db)
):
    new = await crud.create_restaurant(db, payload)
    # clear all restaurant caches
    await FastAPICache.clear(namespace="restaurants")
    return new

@router.get("/", response_model=List[RestaurantResponse])
@cache(namespace="restaurants", expire=300)
async def read_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    start = time.time()
    items = await crud.get_restaurants(db, skip, limit)
    delta = (time.time() - start)*1000
    print(f"🔴 CACHE MISS [list] – {round(delta,2)}ms")
    return items

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
@cache(namespace="restaurants", expire=600)
async def read_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    start = time.time()
    obj = await crud.get_restaurant(db, restaurant_id)
    if not obj:
        raise HTTPException(404, "Restaurant not found")
    delta = (time.time() - start)*1000
    print(f"🔴 CACHE MISS [detail:{restaurant_id}] – {round(delta,2)}ms")
    return obj

@router.get("/search", response_model=List[RestaurantResponse])
@cache(namespace="restaurants", expire=180)
async def search_by_cuisine(
    cuisine: str,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    start = time.time()
    items = await crud.search_restaurants_by_cuisine(db, cuisine, skip, limit)
    delta = (time.time() - start)*1000
    print(f"🔴 CACHE MISS [search:{cuisine}] – {round(delta,2)}ms")
    return items

@router.get("/active", response_model=List[RestaurantResponse])
@cache(namespace="restaurants", expire=240)
async def list_active_restaurants(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    start = time.time()
    items = await crud.get_active_restaurants(db, skip, limit)
    delta = (time.time() - start)*1000
    print(f"🔴 CACHE MISS [active] – {round(delta,2)}ms")
    return items

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(
    restaurant_id: int,
    payload: RestaurantUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await crud.update_restaurant(db, restaurant_id, payload)
    if not updated:
        raise HTTPException(404, "Restaurant not found")
    # invalidate detail + list caches
    await FastAPICache.clear(namespace="restaurants", key=f"read_restaurant:{restaurant_id}")
    await FastAPICache.clear(namespace="restaurants")
    return updated

@router.delete("/{restaurant_id}", response_model=RestaurantResponse)
async def delete_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_restaurant(db, restaurant_id)
    if not deleted:
        raise HTTPException(404, "Restaurant not found")
    # invalidate detail + list caches
    await FastAPICache.clear(namespace="restaurants", key=f"read_restaurant:{restaurant_id}")
    await FastAPICache.clear(namespace="restaurants")
    return deleted
