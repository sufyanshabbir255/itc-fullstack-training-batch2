# create_tables.py - build the tables, add sample data, and show each relationship
from database import SessionLocal, engine, Base
from models import Item, User, UserProfile

# [CREATE TABLES] start clean each run, then create every table from models.py
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("Tables created: users, user_profiles, items, user_favourites")

with SessionLocal() as session:
    # [INSERT] two users
    romesh = User(username="romesh", email="romesh@example.com", full_name="Romesh Bansal")
    sufyan = User(username="sufyan", email="sufyan@example.com", full_name="Muhammad Sufyan")

    # [1 : 1] each user gets exactly one profile
    romesh.profile = UserProfile(bio="Backend tutor", city="Delhi")
    sufyan.profile = UserProfile(bio="Frontend tutor", city="Karachi")

    # [1 : MANY] Romesh owns two items, Sufyan owns one
    laptop = Item(name="Laptop", description="A sample laptop", price=999.99, owner=romesh)
    mouse = Item(name="Mouse", description="A sample mouse", price=25.0, owner=romesh)
    monitor = Item(name="Monitor", description="A sample monitor", price=199.5, owner=sufyan)

    # [MANY : MANY] both users favourite the monitor
    romesh.favourites = [monitor, laptop]
    sufyan.favourites = [monitor]

    session.add_all([romesh, sufyan])
    session.commit()                                  # saves everything in one go

    # [SELECT] read it back through the relationships
    for user in session.query(User).order_by(User.id):
        print(f"\n{user.username} ({user.profile.city}) - {user.profile.bio}")
        print("  owns:      ", [item.name for item in user.items])
        print("  favourites:", [item.name for item in user.favourites])

    monitor = session.query(Item).filter_by(name="Monitor").one()
    print("\nMonitor is favourited by:", [u.username for u in monitor.favourited_by])