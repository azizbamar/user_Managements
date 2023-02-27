
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from fastapi import Depends,APIRouter, HTTPException,Header, Request
from Controllers import UserController,TokenController
from sqlalchemy.orm import Session
# from Controllers.send_email import send_email_async
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Registration import Registration
from Schemas.UpdateUserSchema import UpdateSchema
from database.database import get_db
userRooter = APIRouter()

@userRooter.post('/user_sign_up')
async def signUp(request : Registration, db : Session = Depends(get_db)):
   return  UserController.signUp(request,db)

# Web Sign In
@userRooter.post('/user_sign_in')
async def signIn(request : Authentification, db : Session = Depends(get_db)):
   return  UserController.signIn(request,db)

@userRooter.post('/token_sign_in')
async def signIn(token : str = Header(...)):
   return  TokenController.checkAccessToken(token)


# Phone Sign In
@userRooter.post('/user_sign_in_from_phone')
async def signIn(request : PhoneAuthentification, db : Session = Depends(get_db)):
   return  UserController.signInFromPhone(request,db)

# Web Sign Out
@userRooter.post('/user_sign_out')
async def signIn(db : Session = Depends(get_db),token : str = Header(...)):
   return  UserController.signOut(db,token)

# Phone Sign Out
@userRooter.post('/user_sign_out_from_phone')
async def logout(db : Session = Depends(get_db),token : str = Header(...)):
   return  UserController.signOutFromPhone(db,token)

#update account
@userRooter.post('/update_account')
async def updateUser(request : Registration,db : Session = Depends(get_db),token : str = Header(...)):
   return  UserController.updateUser(request,token,db)

#delete Phone
@userRooter.post('/removePhone/{user_id}')
async def deletePhone(user_id:int,db : Session = Depends(get_db)):
   return  UserController.removePhoneForUser(user_id,db)

# chercher users

@userRooter.get('/users/{name}')
async def deletePhone(name:str,db : Session = Depends(get_db)):
   return  UserController.getUsesrByName(name,db)


@userRooter.post('/phone_token_sign_in')
async def signIn(token : str = Header(...)):

   return  TokenController.checkPhoneAccessToken(token)

@userRooter.patch('/admin/update/{id}')

async def adminUpdateUser(request :UpdateSchema,id,token : str = Header(...), db : Session = Depends(get_db)):

   return  UserController.adminUpdateUser(id,db,request,token)

@userRooter.get('/admin')
async def isAdmin(token : str = Header(...),db : Session = Depends(get_db)):

   return  UserController.isAdmin(db,token=token)

@userRooter.post('/forget_password')
async def reset_password(email :str , db : Session = Depends(get_db)):
   return  UserController.resetPassword(email,db)

#check token validity
@userRooter.post('/phone_check_token')
async def check_token(db : Session = Depends(get_db),token : str = Header(...)):
   #print(f"{Header}")
   return  TokenController.checkPhoneAccessToken(token,db)



@userRooter.get('/getAllUsers')
async def getAllUsers(page:int,limit:int,db : Session = Depends(get_db)):
   return  UserController.getAllUsers(limit,db,page)

@userRooter.delete('/deleteUser/{id}')
async def delete_user(id:int,db : Session = Depends(get_db)):
   return  UserController.deleteUser(id,db)

@userRooter.get('/')
async def home():
   return  "Welcome"



