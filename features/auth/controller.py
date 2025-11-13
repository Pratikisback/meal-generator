
from sqlalchemy.orm import Session
from sqlalchemy import select
from features.user.schema import UserCreate, UserLogin
from features.user.model import User
from core.security import hash_password, create_access_token
from core.database import get_db
from core.response import Response
import bcrypt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import HTTPException
from core.security import decode_token
from jose import jwt, JWTError, ExpiredSignatureError
load_dotenv()


def register_user(user: UserCreate, db: Session):
    response = Response()

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return response.set(status="user already exists", status_code=409, message="User already exists")

    new_user = User(
        email=user.email,
        name=user.name,
        password=hash_password(user.password),
        role=user.role,
        is_deleted=user.is_deleted
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return response.set(status="success", status_code=200, message="User registered successfully", data=new_user)


def login(user: UserLogin, db: Session):
    response = Response()
    pipeline_statement = select(User).where(User.email == user.email).limit(1)
    user_details = db.execute(pipeline_statement).scalars().first()
    print(user_details.email)
    # user_details = db.query(User).filter(User.email == user.email).first()
    if not user_details:
        return response.set(status="user not found", status_code=404, message="User not found")
    is_valid = bcrypt.checkpw(user.password.encode('utf-8'), user_details.password.encode('utf-8'))
    


    if not is_valid:
        return response.set(status="credentials mismatch", status_code=403, message="password is incorrect")

    db.query(User).filter(User.email == user.email).update({User.on_shift: True}, synchronize_session="fetch")
    db.commit()
    access_token = create_access_token(data={"email": user.email, "role": user_details.role}, expires_delta=timedelta(minutes=15))
    refresh_token = create_access_token(data={"email": user.email, "role": user_details.role}, expires_delta=timedelta(days=30)) 
    
    response_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "email": user.email,
        "role": user_details.role,
            }
    
    print(response_data)
    return response.set(status="success", status_code=201, message="user logged in", data=response_data)


def create_access_token_from_refresh_token(token: str, db:Session):
    try: 
        response = Response()

        payload = decode_token(token)
        print(payload.get("email"), "payload debugging")
        if isinstance(payload, dict) and "error" in payload:
            if payload["error"] == "signature_expired":
                return response.set(status="token expired", status_code=401, message="Token has expired", data=None)
            elif payload["error"] == "invalid_token":
                return response.set(status="invalid token", status_code=401, message="Token is invalid", data=None)
            
        user = db.query(User).filter(User.email == payload.get("email")).first()
        if not user:
            return response.set(status="user not found", status_code=404, message="User not found", data=None)

            
        access_token = create_access_token(data={"email": payload.get("email"), "role": payload.get("role")}, expires_delta=timedelta(minutes=15))
        data = {
           
            "access_token": access_token
        } 
        return response.set(status="success", status_code=200, message="access token created", data=data)
    except ExpiredSignatureError:
        return response.set(status="success", status_code=200, message="Token has expired", data=None)
    except JWTError:
        return response.set(status="invalid token", status_code=401, message="Token is invalid", data=None) 




def get_all_users(db: Session, user:User):
    print(user.email, "current user debugging")
    response = Response()
    users = db.query(User).filter(User.is_deleted == False, User.email != user.email).all()
    return response.set(status="success", status_code=200, message="user data", data=users)

def get_profile_data(db:Session, user: User):
    print(user, "user debugging")
    response = Response()
    user_data = db.query(User).filter(User.email == user.email).first()
    if not user_data:
        return response.set(status="user not found", status_code=404, message="User not found")
    
    return response.set(status="success", status_code=200, message="User data retrieved successfully", data=user_data)