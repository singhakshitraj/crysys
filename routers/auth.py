from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException,Depends,status,APIRouter
from config.db import db_connect
from utils.password_hash import hash_password,verify_password
from utils.current_user import create_access_token,create_refresh_token
from fastapi import Body,HTTPException,status

router=APIRouter(
    prefix='/auth'
)

@router.post('/register')
def _register(user=Body(),connection=Depends(db_connect)):
    email,password=user.get('email',None),user.get('password',None)
    if email is None or password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'message':'Data Format incorrect!!'})
    with connection.cursor() as cur:
        cur.execute('''
            SELECT * FROM USERS
            WHERE email=%s
        ''',(email,)
        )
        n_user=cur.fetchone()
        if n_user is not None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User Already Exists. Try Logging in.')
        cur.execute('''
            INSERT INTO USERS(email,password)
            VALUES (%s,%s)
            RETURNING *
        ''',(email,hash_password(password))
        )
        new_user=cur.fetchone()
        if new_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to create new User')
        token=create_access_token({"email":email})
        refresh_token=create_refresh_token({"email":email})
        return {
            "email":email,
            "accessToken":token,
            "refreshToken":refresh_token,
            "tokenType":"Bearer"
        }
        
@router.post('/authenticate')
def _login(user=Body(),connection=Depends(db_connect)):
    email,password=user.get('email',None),user.get('password',None)
    if email is None or password is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'message':'Data Format incorrect!!'})
    with connection.cursor() as cur:
        cur.execute('''
            SELECT * FROM USERS
            WHERE email=%s
        ''',(email,)
        )
        db_user=cur.fetchone()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='No User Found. Check details again.')
        if not verify_password(password,db_user['password']):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect Credentials')
        token=create_access_token({"email":email})
        refresh_token=create_refresh_token({"email":email})
        print(refresh_token)
        return {
            "email":email,
            "accessToken":token,
            "refreshToken":refresh_token,
            "tokenType":"Bearer"
        }