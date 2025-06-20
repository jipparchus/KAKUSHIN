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

from backend.config import load_config


def get_engine():
    config = load_config()
    engine = create_engine(
        config['database']['uri'],
        connect_args={'check_same_thread': False},  # required for sqlite
        echo=False,
        )
    return engine


def get_session_local():
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()
