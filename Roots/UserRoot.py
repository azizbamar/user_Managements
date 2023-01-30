import bcrypt
import jwt
import time
from fastapi import FastAPI,Depends,HTTPException,APIRouter
from Controllers import UserController
from sqlalchemy.orm import Session
from Schemas.Authentification import Authentification

from Schemas.Registration import Registration
from database.database import SessionLocal
userRooter = APIRouter()
def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

@userRooter.post('/user_sign_up')
async def signUp(request : Registration, db : Session = Depends(get_db)):
   return  UserController.signUp(request,db)


@userRooter.post('/user_sign_in')
async def signUp(request : Authentification, db : Session = Depends(get_db)):
   return  UserController.signIn(request,db)
