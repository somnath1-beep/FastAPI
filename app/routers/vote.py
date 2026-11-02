from fastapi import Depends, APIRouter, HTTPException,status, Response
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models
router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)
@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.VoteCreate,db:Session=Depends(database.get_db),current_user=Depends(oauth2.get_current_user)):
    if not db.query(models.Post).filter(models.Post.id==vote.post_id).first():# check if post exist in post table, user want to vote
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found for voting")
    if vote.dir >=1:
        # here try block is used because if user try to vote same post postgres throw exception 
        try:
            new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return new_vote
        except :
            raise(HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Duplicate action"))
    if vote.dir <1:
        vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id)
        vote_delete=vote_query.first()
        if not vote_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found")
        if vote_delete.user_id==current_user.id:
            vote_query.delete(synchronize_session=False)
            db.commit()
        return {"message":"vote deleted"}
