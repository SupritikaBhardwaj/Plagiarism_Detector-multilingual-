from datetime import datetime, timedelta, timezone
import os

from jose import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(subject: str, minutes: int = 60) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return jwt.encode({"sub": subject, "exp": expires_at}, JWT_SECRET, algorithm=ALGORITHM)

