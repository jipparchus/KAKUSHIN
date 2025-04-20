from fastapi import APIRouter, HTTPException
from auth.jwt_utils import create_token
from auth.hashing import hash_password, verify_password
from db.models import User
from db.session import SessionLocal
from db.schemas import AuthData


router = APIRouter()


@router.post('/register')
def register(data: AuthData):
    """
    On Sign up
    """
    hashed_pw = hash_password(data.password)
    # Check with the DB
    rdb = SessionLocal()
    # Already exist user
    if rdb.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=400, detail='Username exists')
    user = User(username=data.username, hashed_password=hashed_pw)
    rdb.add(user)
    print('######################################')
    print(user.id)
    rdb.commit()
    token = create_token({'user_id': user.id})
    return {'access_token': token}


@router.post('/login')
def login(data: AuthData):
    """
    On Sign in
    """
    rdb = SessionLocal()
    user = rdb.query(User).filter_by(username=data.username).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_token({'user_id': user.id})
    return {'access_token': token}
