"""
Session objects enable 'active connection' to the RDB.
- Query tables
- Add rows
- Commit changes
- Rollback on error

e.g.

db = SessionLocal()      # ← creates a session
db.add(new_user)         # ← stage change
db.commit()              # ← write to DB
rdb.close()
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config

engine = create_engine(config['database']['uri'], echo=True)
SessionLocal = sessionmaker(bind=engine)
