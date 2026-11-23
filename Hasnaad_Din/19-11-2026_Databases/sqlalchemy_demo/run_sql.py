# run_sql.py - run plain SQL against the existing tables (read only, nothing is rebuilt)
from sqlalchemy import text

from database import engine

sql = """
SELECT u.id, u.username, i.name AS favourite
FROM users u
JOIN user_favourites f ON f.user_id = u.id
JOIN items i ON i.id = f.item_id
ORDER BY u.id, i.name;
"""

with engine.connect() as conn:
    result = conn.execute(text(sql))
    print(list(result.keys()))
    for row in result:
        print(row)