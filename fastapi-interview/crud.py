from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User, UserPost

async def get_user(db: AsyncSession, user_id: int) -> User | None:
    """Return the User object or None if not found."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_posts_by_user(db: AsyncSession, user_id: int) -> list[UserPost]:
    """Return all posts for the given user_id."""
    result = await db.execute(
        select(UserPost).where(UserPost.user_id == user_id)
    )
    return result.scalars().all()

async def create_post(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: str
) -> UserPost:
    """Create a new post for a given user."""
    post = UserPost(title=title, description=description, user_id=user_id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post
