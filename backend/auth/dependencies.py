from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_utils import decode_token
from db.session import SessionLocal
from db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_token(token)
    if payload is None or 'user_id' not in payload:
        raise HTTPException(status_code=401, detail='Invalid token')

    db = SessionLocal()
    user = db.query(User).filter(User.uuid == payload['user_id']).first()
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    return user
