"""
Dependency is a reusable logic that FastAPI can inject into the route functions.

e.g.
from sqlalchemy.orm import Session
from fastapi import Depends

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db.add(...)
"""

from db.session import SessionLocal


def get_db():
    db = SessionLocal()     # Create DB session
    try:
        yield db            # Provide it to the route
    finally:
        db.close()
