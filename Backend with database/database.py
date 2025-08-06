from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Step 1
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Step 2
engine = create_async_engine(
    DATABASE_URL,
    echo= True, # Shows SQL queries in console
    future = True # Important in older versions, enables SQLAlchemy 2.0 style behavior in SQLAlchemy 1.4+
)

# Step 3 - Create session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_= AsyncSession, # AsyncSession -> creates session object
    expire_on_commit=False
)

Base = declarative_base()

# get_db is the bridge between routers and database file
async def get_db():
    """
    Dependancy that provides database session to FastAPI endpoints
    This ensures proper session lifecycle management
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session # Provide session to endpoint
        except Exception as e:
            await session.rollback() # Rollback on error
            raise e
        finally:
            await session.close() # Always close session

# yield -> unlike return, yield will allow the further operation after THAT line.

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
