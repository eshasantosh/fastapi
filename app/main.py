from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas    #the . represents the current folder that this file is in
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

#connecting to db
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user ='postgres', password='esha123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful.")
        break
    except Exception as error:
        print("Connection to database failed.")
        print("Error: ", error)
        time.sleep(5)

app = FastAPI()     # created instance of FastAPI

@app.get("/")       # decorator w instance and endpt. 'get' request is http method. '/' is root path
def root():   #or 'async def' keyword optional
    return {"message": "Hello World"}

@app.get("/posts", response_model=List[schemas.Post])  #order of paths coded matters. will retrieve first matching path oprn
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all() #.all sends the query
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)  
def create_posts(post : schemas.PostCreate, db: Session = Depends(get_db)): #Post is our pydantic model user defined data type, post is the var name
    new_post = models.Post(**post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #retrieve into newpost var after committing it
    return new_post

#for urls use plural bec convntn
@app.get("/posts/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):   #fastapi extracts the id. converts to int
    post = db.query(models.Post).filter(models.Post.id == id).first() #bec only one, we k
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) #dont return json for http204 in fastapi

@app.put("/posts/{id}", response_model= schemas.Post) #response_model= schemas.Post NOT WORKING
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_query.update(updated_post.model_dump(), synchronize_session=False) 
    db.commit()
    return post

'''
notes
sqlalchemy not part of fastapi
to use it with postgres, need psycopg2

schema/pydantic model Post to define expected parameters etc
orm model/sqlachemy model Post has attributes reqd acc to table in db
'''