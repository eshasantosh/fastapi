from fastapi import FastAPI
from . import models            #the . represents the current folder that this file is in
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()     # created instance of FastAPI

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
