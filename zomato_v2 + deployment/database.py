# database.py
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 1. Database URL (SQLite file in current dir)
DATABASE_URL = "sqlite+aiosqlite:///./restaurants.db"

# 2. Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,       # show SQL in console
    future=True      # use SQLAlchemy 2.0 style
)

# 3. Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Base class for our models
Base = declarative_base()

# 5. Dependency for FastAPI endpoints
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()

# 6. Helper to create all tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
