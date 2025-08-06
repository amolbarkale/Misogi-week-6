from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from database import get_db
from schemas import UserResponse
from models import User
import crud

user_router = APIRouter(prefix="/user", tags=["users"])

@user_router.get("/", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_users(db, skip=skip, limit=limit)

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.dict())

    db_user = {
        "username": "xyz",
        "email": "xyz@mail"
        "fullname"
    }

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
