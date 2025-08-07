from fastapi import FastAPI
import uvicorn
import time

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from database import create_tables, get_db
from routes.restaurants import router as restaurant_router

app = FastAPI(
    title="Zomato v2 – Redis Caching (Version 1)",
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    # init DB
    await create_tables()

    # init Redis + cache
    redis = aioredis.from_url(
        "redis://localhost:6379", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="zomato-cache")
    print("✅ Redis cache initialized")

# include our restaurants router
app.include_router(restaurant_router)

# -- Cache Management Endpoints --

@app.get("/cache/stats")
async def cache_stats():
    backend = FastAPICache.get_backend().redis
    keys = await backend.keys("zomato-cache:*")
    return {
        "cache_size": len(keys),
        "cache_keys": keys,
        "note": "Use redis-cli KEYS for full listing"
    }

@app.delete("/cache/clear")
async def clear_all_cache():
    await FastAPICache.clear()
    return {"message": "✅ Cleared entire cache"}

@app.delete("/cache/clear/restaurants")
async def clear_restaurant_cache():
    await FastAPICache.clear(namespace="restaurants")
    return {"message": "✅ Cleared restaurant-related caches"}

# -- Demo & Sample Data --

@app.post("/demo/sample-data")
async def create_sample_data(db=Depends(get_db)):
    sample = [
        {"name":"Pasta Palace","cuisine_type":"Italian","address":"…","phone_number":"+12345","opening_time":"11:00","closing_time":"22:00"},
        {"name":"Sushi Central","cuisine_type":"Japanese","address":"…","phone_number":"+67890","opening_time":"12:00","closing_time":"23:00"},
        # …more…
    ]
    created = []
    for data in sample:
        # naïve dedupe on name
        existing = await crud.search_restaurants_by_cuisine(
            db, cuisine=data["name"], skip=0, limit=1
        )
        if not any(r.name==data["name"] for r in existing):
            await crud.create_restaurant(db, RestaurantCreate(**data))
            created.append(data["name"])
    # invalidate namespace
    await FastAPICache.clear(namespace="restaurants")
    return {"created": created}

@app.get("/demo/cache-test/{restaurant_id}")
async def demo_cache_test(restaurant_id: int, db=Depends(get_db)):
    from routes.restaurants import read_restaurant
    results = []
    for i in range(1, 4):
        start = time.time()
        try:
            res = await read_restaurant(restaurant_id, db)
            delta = (time.time() - start)*1000
            status = "HIT" if i>1 else "MISS"
            results.append({
                "attempt": i,
                "status": status,
                "time_ms": round(delta,2),
                "name": res.name
            })
        except:
            results.append({"attempt": i, "error": "Not found"})
            break
    return {"performance": results}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
