"""
Module related to JWT access token

1. Create token
2. Validate token
"""

# import jwt
from jose import jwt
from datetime import datetime, timedelta
from config import config

SECRET_KEY = config['secret']['jwt_key']
ALGORITHM = "HS256"
EXPIRY_MINUTES = 30

# Generate token


def create_token(data: dict):
    data_copy = data.copy()
    data_copy["user_id"] = str(data_copy["user_id"])
    data_copy["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRY_MINUTES)
    return jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)

# Decode and validate token


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
