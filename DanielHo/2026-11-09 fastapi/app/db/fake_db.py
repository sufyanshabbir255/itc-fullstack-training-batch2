"""
app/db/fake_db.py
-----------------
A tiny IN-MEMORY "database" so the project runs with zero setup.

    - Data lives in Python dicts, so it resets every time the server restarts.
    - Swapping this for a real database (PostgreSQL + SQLAlchemy, etc.) would
      only require changing this layer; routers and schemas stay the same.
      That separation is the whole point of having a `db` folder.
"""

from datetime import datetime, timezone
from itertools import count

# --- Items ---------------------------------------------------------------
# key = item id, value = dict of item fields
items_db: dict[int, dict] = {}
_item_id_counter = count(start=1)  # generates 1, 2, 3, ... like AUTO_INCREMENT

# --- Users ---------------------------------------------------------------
users_db: dict[int, dict] = {}
_user_id_counter = count(start=1)


def next_item_id() -> int:
    return next(_item_id_counter)


def next_user_id() -> int:
    return next(_user_id_counter)


def fake_hash_password(password: str) -> str:
    """
    NOT REAL SECURITY – for demonstration only.
    In production use passlib/bcrypt or argon2.
    """
    return "hashed_" + password[::-1]


def seed_data() -> None:
    """Put a few sample records in so GET endpoints return something right away."""
    if items_db:
        return  # already seeded
    for name, price in [("Laptop", 999.99), ("Mouse", 25.0), ("Monitor", 199.5)]:
        item_id = next_item_id()
        items_db[item_id] = {
            "id": item_id,
            "name": name,
            "description": f"A sample {name.lower()}",
            "price": price,
            "in_stock": True,
            "created_at": datetime.now(timezone.utc),
        }
