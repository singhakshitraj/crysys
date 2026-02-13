from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException,Depends,status,APIRouter, Body
from utils.password_hash import hash_password,verify_password
from utils.current_user import create_access_token,create_refresh_token
from fastapi import Body,HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.db import db_connection
from models.user import User
router=APIRouter(
    prefix='/auth'
)

@router.post("/register")
def register(
    user: dict = Body(),
    db: Session = Depends(db_connection)
):
    email = user.get("email")
    password = user.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Data Format incorrect!!"}
        )
    stmt = select(User).where(User.email == email)
    existing_user = db.scalar(stmt)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User Already Exists. Try Logging in."
        )
    new_user = User(
        email=email,
        password=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"email": new_user.email})
    refresh_token = create_refresh_token({"email": new_user.email})

    return {
        "email": new_user.email,
        "accessToken": token,
        "refreshToken": refresh_token,
        "tokenType": "Bearer"
    }

        
@router.post("/authenticate")
def login(
    user: dict = Body(),
    db: Session = Depends(db_connection)
):
    email = user.get("email")
    password = user.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Data Format incorrect!!"}
        )
    stmt = select(User).where(User.email == email)
    db_user = db.scalar(stmt)

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No User Found. Check details again."
        )
    if not verify_password(password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Credentials"
        )
    token = create_access_token({"email": db_user.email})
    refresh_token = create_refresh_token({"email": db_user.email})

    return {
        "email": db_user.email,
        "accessToken": token,
        "refreshToken": refresh_token,
        "tokenType": "Bearer"
    }