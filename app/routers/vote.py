from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2, database

router = APIRouter(
    prefix="/vote",
    tags=["vote"] #what were the tags for?
)

@router.post("/", status_code=status.HTTP_201_CREATED) 
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == vote.user_id)       #check whether the vote exists
    found_vote = vote_query.first
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f'User {vote.user_id} has already voted on post {vote.post_id}.')
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully added vote'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'Vote does not exist.')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'successfully deleted vote'}