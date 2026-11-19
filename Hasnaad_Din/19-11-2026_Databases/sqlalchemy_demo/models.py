# models.py - the tables, written as Python classes
# Users and Items use the SAME field names as the FastAPI app (fake_db.py)
from datetime import datetime, timezone

from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


from database import Base

# [MANY : MANY] link table: one user can favourite many items, one item can be favourited by many users
user_favourites = Table(
    "user_favourites",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("item_id", ForeignKey("items.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)                        # [PRIMARY KEY]
    username = Column(String(30), unique=True, nullable=False, index=True)  # [INDEX]
    email = Column(String(255), unique=True, nullable=False, index=True)    # [INDEX]
    full_name = Column(String(100))

    profile = relationship("UserProfile", back_populates="user", uselist=False)  # [1 : 1]
    items = relationship("Item", back_populates="owner")                         # [1 : MANY]
    favourites = relationship("Item", secondary=user_favourites, back_populates="favourited_by")  # [MANY : MANY]

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    bio = Column(String(500))
    city = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # [FOREIGN KEY] unique = 1:1

    user = relationship("User", back_populates="profile")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)                        # [PRIMARY KEY]
    name = Column(String(100), nullable=False, index=True)        # [INDEX]
    description = Column(String(500))
    price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))            # [FOREIGN KEY] not unique = 1:many

    owner = relationship("User", back_populates="items")
    favourited_by = relationship("User", secondary=user_favourites, back_populates="favourites")