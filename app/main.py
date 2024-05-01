from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils    #the . represents the current folder that this file is in
from .database import get_db, engine
from .routers import post, user, auth

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
def root():         #or 'async def' keyword optional
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
