from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth.jwt_utils import create_token
from db.models import User
from db.session import SessionLocal

router = APIRouter()


class AuthData(BaseModel):
    username: str
    password: str


@router.post('/register')
def register(data: AuthData):
    """
    On Sign up
    """
    # Check with the DB
    db = SessionLocal()
    # Already exist user
    if db.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=400, detail='Username exists')
    user = User(username=data.username, password=data.password)
    db.add(user)
    db.commit()
    return {'status': 'registered'}


@router.post('/login')
def login(data: AuthData):
    """
    On Sign in
    """
    db = SessionLocal()
    user = db.query(User).filter_by(username=data.username, password=data.password).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_token({'user_id': user.id})
    return {'token': token}
