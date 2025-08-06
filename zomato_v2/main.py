from fastapi import FastAPI
import uvicorn

from database import create_tables
from routes.restaurants import router as restaurants_router
from routes.menu_items import router as menu_items_router

app = FastAPI(
    title="Zomato v2: Restaurant & Menu Management",
    description="CRUD API with one-to-many relationships",
    version="2.0.0"
)

@app.on_event("startup")
async def on_startup():
    await create_tables()

app.include_router(restaurants_router)
app.include_router(menu_items_router)

@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to Zomato v2 API!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
