from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User

def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()
