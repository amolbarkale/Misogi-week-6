from fastapi import FastAPI, Depends, HTTPException
from starlette.status import HTTP_201_CREATED
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uvicorn

from databse import create_tables, get_db
import crud

app = FastAPI(title="User-Post App")

@app.on_event("startup")
async def on_startup():
    # Create tables if they don't exist
    await create_tables()

@app.post(
    "/posts/{user_id}",
    status_code=HTTP_201_CREATED,
    summary="Create a post for a user"
)
async def add_post(
    user_id: int,
    title: str,
    description: str,
    db: AsyncSession = Depends(get_db)
):
    # 1) Verify user exists
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2) Create the post
    post = await crud.create_post(db, user_id, title, description)

    # 3) Return a simple dict
    return {
        "id": post.id,
        "title": post.title,
        "description": post.description,
        "user_id": post.user_id
    }

@app.get(
    "/posts/{user_id}",
    summary="List all posts for a user"
)
async def read_posts(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    # 1) Verify user exists
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2) Fetch posts
    posts = await crud.get_posts_by_user(db, user_id)

    # 3) Return as list of dicts
    return [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "user_id": p.user_id
        }
        for p in posts
    ]

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
