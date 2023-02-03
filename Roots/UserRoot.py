import bcrypt
import jwt
import time
from fastapi import FastAPI,Depends,HTTPException,APIRouter,Header
from models.User import user_roles
from Controllers import UserController
from sqlalchemy.orm import Session
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
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
# Web Sign In
@userRooter.post('/user_sign_in')
async def signIn(request : Authentification, db : Session = Depends(get_db)):
   return  UserController.signIn(request,db)
# Phone Sign In
@userRooter.post('/phone/user_sign_in')
async def signIn(request : PhoneAuthentification, db : Session = Depends(get_db)):
   return  UserController.PhonesignIn(request,db)


@userRooter.post('/user_sign_out')
async def signUp(db : Session = Depends(get_db),token : str = Header(...)):
   return  UserController.signOut(db,token)
