import bcrypt
import jwt
import time
from fastapi import FastAPI,Depends,HTTPException,APIRouter
from Controllers import UserController
userRooter = APIRouter()


@userRooter.post('/user_sign_up')
async def signUp():
   return  UserController.signUp()
