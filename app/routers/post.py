from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, oauth2   # the .. means one folder back in hierarchy
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])   #order of paths coded matters. will retrieve first matching path oprn
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #data type of current_user doesnt matter here
    posts = db.query(models.Post).all()                 #.all sends the query
    #posts = db.query(models.Post).filter(models.Post.id == current_user.id).all()  #if you want to retrieve only the logged in users own posts
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)  
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    new_post = models.Post(owner_id = current_user.id, **post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #retrieve into newpost var after committing it
    return new_post

@router.get("/{id}", response_model= schemas.Post)                   #for urls use plural bec convntn
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):                   #fastapi extracts the id. converts to int
    post = db.query(models.Post).filter(models.Post.id == id).first()   #bec only one, we k
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action.")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) #dont return json for http204 in fastapi

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action.")

    post_query.update(updated_post.model_dump(), synchronize_session=False) 
    db.commit()
    return post