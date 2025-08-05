# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# engine = create_async_engine(
#     DATABASE_URL,
#     echo= True, # enables SQL logging
#     future = True # important in older versions, enables SQLAlchemy 2.0 style behavior in SQLAlchemy 1.4+
# )

# AsyncSessionLocal = async_sessionmaker(
#     engine,
#     class_= AsyncSession,
#     expire_on_commit=False
# )

# Base = declarative_base()