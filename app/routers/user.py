from .. import schemas,utils,models 
from fastapi import FastAPI, Response, status , HTTPException,Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    prefix='/users',
    tags=["user"]
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.CreateUser,db:Session=Depends(get_db)):
    hashed_pwd= utils.hash(user.password)
    new_user=models.User(email=user.email,password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 
@router.get('/{id}',status_code=status.HTTP_302_FOUND,response_model=schemas.UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    db_user=db.query(models.User).filter(models.User.id==id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
    return db_user