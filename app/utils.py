
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password) :
    return pwd_context.hash(password)


def verify(plain_text, hashed):
    return pwd_context.verify(plain_text, hashed)