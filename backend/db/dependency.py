"""
Dependency is a reusable logic that FastAPI can inject into the route functions.

e.g.
from sqlalchemy.orm import Session
from fastapi import Depends

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db.add(...)
"""

from backend.db.session import get_session_local


def get_db():
    db = get_session_local()
    try:
        yield db
    finally:
        db.close()  # Clean up
