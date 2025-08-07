# main.py

from fastapi import FastAPI
import uvicorn

from database import create_tables
from routes import router as restaurant_router
from database import create_tables

app = FastAPI(
    title="Zomato v1: Restaurant Management",
    description="Basic CRUD API for managing restaurants",
    version="1.0.0"
)

# 1. Create tables on startup
@app.on_event("startup")
async def on_startup():
    await create_tables()

# 2. Include our restaurants router
app.include_router(restaurant_router)

# 3. Root health-check endpoint
@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to Zomato v1 API!"}

# 4. If run directly, start Uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
