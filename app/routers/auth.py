from fastapi import Depends, HTTPException,APIRouter,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils
from ..import oauth2
router=APIRouter(tags=["Authentication"])
@router.post('/login')
def login_user(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(database.get_db)):
    # {     oAuth2passwordRequestform send data in this form
    #     "username":"",
    #     "password":""
    # }
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first() 
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    jwt = oauth2.create_access_token({"user_id":user_credentials.username})
    return {"access_token":jwt,"token_type":"bearer"} 