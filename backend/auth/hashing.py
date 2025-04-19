from passlib.context import CryptContext

# Hash config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Encoding


def hash_password(password: str):
    return pwd_context.hash(password)

# Decoding


def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)
