from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils   # the .. means one folder back in hierarchy
from ..database import get_db

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)  
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hashing pw
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut) 
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found.")
    return user


# '''
# notes
# sqlalchemy not part of fastapi
# to use it with postgres, need psycopg2

# schema/pydantic model Post to define expected parameters etc
# orm model/sqlachemy model Post has attributes reqd acc to table in db
# '''