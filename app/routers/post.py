from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional, List
from .. import models, schemas, utils   # the .. means one folder back in hierarchy
from ..database import get_db

router = APIRouter()

@router.get("/posts", response_model=List[schemas.Post])   #order of paths coded matters. will retrieve first matching path oprn
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()                 #.all sends the query
    return posts

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)  
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)): #Post is our pydantic model user defined data type, post is the var name
    new_post = models.Post(**post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #retrieve into newpost var after committing it
    return new_post

@router.get("/posts/{id}", response_model= schemas.Post)                   #for urls use plural bec convntn
def get_post(id: int, db: Session = Depends(get_db)):                   #fastapi extracts the id. converts to int
    post = db.query(models.Post).filter(models.Post.id == id).first()   #bec only one, we k
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post
    

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) #dont return json for http204 in fastapi

@router.put("/posts/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_query.update(updated_post.model_dump(), synchronize_session=False) 
    db.commit()
    return post