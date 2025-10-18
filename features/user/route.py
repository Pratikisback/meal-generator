from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from core.database import get_db
from features.user import controller, schema
from features.user.model import User
from dependencies.auth import get_current_user
from fastapi import HTTPException
from core.response import Response
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user_data: schema.UserCreate, db: Session = Depends(get_db)):
    return controller.register_user(user_data, db)


@router.post("/login")
def login_user(user_data: schema.UserLogin, db: Session = Depends(get_db)):
    result = controller.login(user_data, db)

    if result["status"] != "success":
        return JSONResponse(status_code=result["status_code"], content=result)

    access_token = result["data"]["access_token"]
    refresh_token = result["data"]["refresh_token"]

    response = JSONResponse(status_code=201, content=result)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="none",
        secure=False  # Use False if testing on localhost with HTTP and True if in production with HTTPS
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=False  # Use False if testing on localhost with HTTP and True if in production with HTTPS
    )

    print(response.headers, "response headers")


    return response 


@router.get("/get-all-users")
async def get_all_users(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return controller.get_all_users(db, current_user)

@router.post("/create-access-token")
async def create_access_token_from_refresh_token(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        return JSONResponse(content={
            "status": "Missing refresh token",
            "status_code": 400,
            "message": "Missing refresh token",
            "data": None
        }, status_code=400)

    result = controller.create_access_token_from_refresh_token(token, db)
    result = dict(result)
    if result.get("status_code") == 200 and result.get("data") and result.get("data").get("access_token"):
        response = JSONResponse(content=result, status_code=200)
        response.set_cookie(
            key="access_token",
            value=result.get("data").get("access_token"),
            httponly=True,
            samesite="lax",
            max_age=15 * 60  
        )
        return response

    return JSONResponse(content=result, status_code=result.get("status_code"))
@router.post("/get-profile-data")
async def get_profile_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return controller.get_profile_data(db, current_user)
    
    