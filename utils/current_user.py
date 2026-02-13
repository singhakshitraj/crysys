from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from datetime import datetime,timedelta
import jwt,os
from config.db import db_connection
from models.user import User
from sqlalchemy import select
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data:dict):
    data.update({'exp':datetime.now()+timedelta(minutes=90)})
    return jwt.encode(
        data,
        key=os.environ.get('SECRET_KEY') or "",
        algorithm="HS256",
    )

def create_refresh_token(data:dict):
    data.update({'exp':datetime.now()+timedelta(days=90)})
    return jwt.encode(
        data,
        key=os.environ.get('SECRET_KEY') or "",
        algorithm="HS256",
    )

def get_current_user(token=Depends(oauth2_bearer),session=Depends(db_connection)):
    load_dotenv()
    data=jwt.decode(token,key=os.environ.get('SECRET_KEY') or "",algorithms=[os.environ.get('ALGORITHM') or ""])
    if data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Incorrect Token!')
    stmt = select(User).where(User.email == data['email'])
    user_id = session.execute(stmt).scalar_one().id
    return user_id