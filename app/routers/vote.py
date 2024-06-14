from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database

router = APIRouter(
    prefix="/vote",
    tags=["vote"] #what were the tags for?
)

@router.post("/", status_code=status.HTTP_201_CREATED) 
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} doesn't exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)       #check whether the vote exists
    found_vote = vote_query.first()
    if (vote.dir == 1): #add vote
        if found_vote:  #cant add multiple votes
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'User {current_user.id} has already voted on post {vote.post_id}.')
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully added vote'}
    else:   #to remove vote
        if not found_vote:  #no vote to remove
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Vote does not exist.')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'successfully deleted vote'}