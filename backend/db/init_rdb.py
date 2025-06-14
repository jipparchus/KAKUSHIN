"""
Create a SQLite database based on /models.py
"""
import os
from sqlalchemy import create_engine

from config import config

# DATABASE MODELS
from db.models import Base


def main():
    if os.path.exists(config['paths']['database']):
        return 0
    else:
        engine = create_engine(
            config['database']['uri'],
            echo=True
        )
        # CREATE TABLES
        Base.metadata.create_all(engine)
        return 0


if __name__ == '__main__':
    main()
