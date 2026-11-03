from .. import schemas,utils,models, oauth2
from fastapi import FastAPI, Response, status , HTTPException,Depends,APIRouter
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, MappingResult
router = APIRouter(
    prefix='/posts',
    tags=["posts",]
)

# sqlalchemy
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.CreatePost,db:Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    #new_post=models.user(**dict(post))
    # print(current_user) 
    new_post=models.Post(title=post.title,content=post.content,owner_id=current_user.id)#return class instance before addind to database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#return class instance adding to database
    #print(new_post.created_at)
    return new_post

# @router.get('/',status_code=status.HTTP_202_ACCEPTED,response_model=List[schemas.PostResponse])
@router.get('/',status_code=status.HTTP_202_ACCEPTED,response_model=List[schemas.VoteResponse]) 
def get_all_post(db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user),limit:int=10, 
                 skip:int=0,search:Optional[str]=""): 
    # cursor.execute('SELECT*FROM product')
    # posts=cursor.fetchall()
    # print(posts)
    # return posts
# @router.get('/posts/latest')
# def root():
#     return {'message':'latest post'}
    #new_post=db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    #new_post=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    new_post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if not new_post:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    return new_post
@router.get('/{id}',status_code=status.HTTP_302_FOUND,response_model=schemas.VoteResponse)
# def get_latest_post(id:int,response:Response):# response:Response mean Response instance is passed to the function and we can use it to set the status code of the response
#     if id>=len(post_info):
#         #response.status_code = 404
#         response.status_code=status.HTTP_404_NOT_FOUND
#         # instead of use these above code for showing error to client we can use shortcut using HTTPException
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='resource not found')
#         return {'error':'post not found'}
#     else:
#         return post_info[id]

# sqlalchemy
def get_post_by_id(id:int,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):# current_user get instance of User class
    # new_post=db.query(models.Post).filter(models.Post.id==id).first()
    new_post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).outerjoin(models.Vote,models.Post.id==models.Vote.post_id).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not new_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    # if new_post.owner_id !=current_user.id:
    #      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="owner not found")
         
    print(new_post)
    return new_post

@router.put('/{id}',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def update_post(id:int, post:schemas.CreatePost,db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    #  cursor.execute("UPDATE product SET name = %s, price=%s WHERE id =%s RETURNING *",(post.title,post.content,str(id)))
    #  updated=cursor.fetchone()
    #  conn.commit() 
    #  print(updated)
    #  if updated == None:
    #      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #  return updated
    post_query=db.query(models.Post).filter(models.Post.id==id)
    new_post=post_query.first()
    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    if new_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOt authorized to perform requested action")
    post_query.update({"title":post.title,"content":post.content},synchronize_session=False)
    db.commit()
    return new_post


@router.delete('/{id}',response_model=schemas.PostResponse)# when we use this status code then we can't/don't need to return any reponse from  the function. it won't shown in client side in postman
# def delete_post(id:int):
#     cursor.execute("DELETE FROM product WHERE id = %s RETURNING *",(str(id)))
#     deleted=cursor.fetchone()
#     print(deleted)
#     conn.commit()
#     print(deleted)
#     return deleted

# sqlalchemy   
def delete_post(id:int, db:Session=Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    # new_post= db.query(models.user).filter(models.user.id==id).first()
    new_post= db.get(models.Post,ident=id)
    if new_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if new_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="NOt authorized to perform requested action")
    db.delete(new_post)
    db.commit()
    return new_post