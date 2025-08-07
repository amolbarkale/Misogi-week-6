from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey
from databse import Base

class User(Base):
    __tablename__ = "user_account"

    id          : Mapped[int]     = mapped_column(Integer, primary_key=True, index=True)
    username    : Mapped[str]     = mapped_column(String(30), unique=True, nullable=False)
    email       : Mapped[str]     = mapped_column(String(100), unique=True, nullable=False)
    is_verified : Mapped[bool]    = mapped_column(Boolean, default=False, nullable=False)
    password    : Mapped[str]     = mapped_column(String, nullable=False)

    # one-to-many relationship: a User has many posts
    posts       : Mapped[list["UserPost"]] = relationship(
        "UserPost", back_populates="user", cascade="all, delete-orphan"
    )


class UserPost(Base):
    __tablename__ = "user_post"

    id          : Mapped[int]     = mapped_column(Integer, primary_key=True, index=True)
    title       : Mapped[str]     = mapped_column(String(200), nullable=False)
    description : Mapped[str]     = mapped_column(Text, nullable=True)

    user_id     : Mapped[int]     = mapped_column(
        Integer, ForeignKey("user_account.id", ondelete="CASCADE"), nullable=False
    )

    # many-to-one relationship: each post belongs to one user
    user        : Mapped[User]    = relationship(
        "User", back_populates="posts"
    )
