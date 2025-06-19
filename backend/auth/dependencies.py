from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from auth.jwt_utils import decode_token
from uuid import UUID
from db.models import User
from db.dependency import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    payload = decode_token(token)
    if payload is None or 'user_id' not in payload:
        raise HTTPException(status_code=401, detail='Invalid token')

    user = db.query(User).filter(User.id == UUID(payload['user_id'])).first()
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    return user
