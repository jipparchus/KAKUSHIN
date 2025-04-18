"""
Create a SQLite database based on /models.py
"""

# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
from sqlalchemy import create_engine

from config import config

# DATABASE MODELS
from db.models import Base


def main():
    engine = create_engine(
        config['database']['uri'],
        echo=True
    )
    # CREATE TABLES
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
