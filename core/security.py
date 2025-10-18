import bcrypt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
import jwt
from jose import jwt, JWTError, ExpiredSignatureError
from core.constants import ADMIN_ROLE_IDENTIFIER, MANAGER_ROLE_IDENTIFIER, USER_ROLE_IDENTIFIER

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role") not in [ADMIN_ROLE_IDENTIFIER, MANAGER_ROLE_IDENTIFIER, USER_ROLE_IDENTIFIER]:
            return {"error": "Invalid role in token"}
        
        return payload

    except ExpiredSignatureError:
        return {"error": "signature_expired"}
    except JWTError:
        return {"error": "invalid_token"}