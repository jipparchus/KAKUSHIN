"""
Dependency is a reusable logic that FastAPI can inject into the route functions.

e.g.
from sqlalchemy.orm import Session
from fastapi import Depends

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db.add(...)
"""

from backend.db.session import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Clean up
