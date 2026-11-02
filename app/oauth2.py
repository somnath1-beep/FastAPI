from jose import JWTError,jwt
from datetime import datetime, timedelta
from . import schemas, models, database
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from.config import settings
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
#secret key
#Algorithm
#access token expiretime
SECRET_KEY =settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":int(expire.timestamp())})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encode_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM],options={"leeway":0})# payload is dictionary
        # options={"leeway":0} prevent server to give extra 120 second for token to be valid becz by default server keeps 120s for token to be valid
        id = payload.get("user_id")# data is key
        if id == None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(db:Session=Depends(database.get_db),token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not valid credentials"
                                          ,headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token,credentials_exception)
    user_id = db.query(models.User).filter(models.User.email == token_data.id).first()
    if  not user_id:# every time when you use .first() you have to check if it is None to avoid error 
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    return user_id