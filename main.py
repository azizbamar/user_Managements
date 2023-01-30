from fastapi import FastAPI,Depends,HTTPException
from database.database import engine,SessionLocal,Base
from models.User import User
from models.Token import Token
from models.Phone import Phone


from sqlalchemy.orm import Session
from Roots.UserRoot import userRooter

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(userRooter)