from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.auth.jwt_utils import create_token
from backend.auth.hashing import hashing, verify_hash
from backend.db.dependency import get_db
from backend.db.models import User
from backend.db.schemas import AuthData


router = APIRouter()


@router.post('/register')
def register(data: AuthData, db: Session = Depends(get_db)):
    """
    On Sign up
    injecting the database session to handle the session lifecycle safely.
    """
    hashed_pw = hashing(data.password)
    # Already exist user
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=400, detail='Username exists')
    user = User(username=data.username, hashed_password=hashed_pw)
    db.add(user)
    print('######################################')
    print(user.id)
    db.commit()
    token = create_token({'user_id': user.id})
    return {'access_token': token}


@router.post('/login')
def login(data: AuthData, db: Session = Depends(get_db)):
    """
    On Sign in
    """
    user = db.query(User).filter_by(username=data.username).first()
    if not user or not verify_hash(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_token({'user_id': user.id})
    return {'access_token': token}
