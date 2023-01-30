from Schemas.Hasher import hash_password
from Schemas.Registration import Registration
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.User import User
from fastapi import FastAPI,Depends,HTTPException


def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

def signUp(request : Registration , db : Session = Depends(get_db)):
    hashed_password = hash_password(request.password)
    user = User(email = request.email , password = hashed_password, username = request.username ,telephoneNumber = request.telephoneNumber)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user