from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

import psycopg2
from psycopg2.extras import RealDictCursor
import time

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}' #postgresql://user:password@postgresserver/db

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# #connecting to db wo sqlachemy. put in main.py
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user ='postgres', password='esha123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection successful.")
#         break
#     except Exception as error:
#         print("Connection to database failed.")
#         print("Error: ", error)
#         time.sleep(5)