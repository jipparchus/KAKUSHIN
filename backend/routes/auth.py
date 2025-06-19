from fastapi import APIRouter, HTTPException
# from backend.auth.jwt_utils import create_token
from backend.auth import jwt_utils
from backend.auth.hashing import hashing, verify_hash
from backend.db.models import User
from backend.db.session import get_session_local
from backend.db.schemas import AuthData


router = APIRouter()


@router.post('/register')
def register(data: AuthData):
    """
    On Sign up
    """
    hashed_pw = hashing(data.password)
    # Check with the DB
    rdb = get_session_local()
    # Already exist user
    if rdb.query(User).filter_by(username=data.username).first():
        raise HTTPException(status_code=400, detail='Username exists')
    user = User(username=data.username, hashed_password=hashed_pw)
    rdb.add(user)
    print('######################################')
    print(user.id)
    rdb.commit()
    token = jwt_utils.create_token({'user_id': user.id})
    return {'access_token': token}


@router.post('/login')
def login(data: AuthData):
    """
    On Sign in
    """
    rdb = get_session_local()
    user = rdb.query(User).filter_by(username=data.username).first()
    if not user or not verify_hash(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = jwt_utils.create_token({'user_id': user.id})
    return {'access_token': token}
