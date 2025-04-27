from passlib.context import CryptContext

# Hash config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Encoding


def hashing(text: str):
    return pwd_context.hash(text)

# Decoding


def verify_hash(plain_text, hashed_text):
    return pwd_context.verify(plain_text, hashed_text)
