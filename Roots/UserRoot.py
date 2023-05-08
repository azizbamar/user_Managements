
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import List, Optional
from fastapi import Body, Depends,APIRouter, File, HTTPException,Header, Request, UploadFile
from Controllers import UserController,TokenController
from sqlalchemy.orm import Session
from sqlalchemy import inspect
# from Controllers.send_email import send_email_async
from Schemas.Authentification import Authentification
from Schemas.EmailSchema import ResetPasswordRequest
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Registration import Registration
from Schemas.SendEmailsSchema import SendEmails
from Schemas.UpdateUserSchema import UpdateSchema
from Schemas.UserChangePasswordSchema import UserChangePasswordSchema
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
async def checkAccessToken(token : str = Header(...)):
   return  TokenController.checkAccessToken(token)


# Phone Sign In
@userRooter.post('/user_sign_in_from_phone')
async def signInFromPhone(request : PhoneAuthentification, db : Session = Depends(get_db)):
   return  UserController.signInFromPhone(request,db)

# Web Sign Out
@userRooter.post('/user_sign_out')
async def signOut(db : Session = Depends(get_db),token : str = Header(...)):
   return  UserController.signOut(db,token)

# Phone Sign Out
@userRooter.post('/user_sign_out_from_phone')
async def signOutFromPhone(db : Session = Depends(get_db),token : str = Header(...)):
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
async def getUsersByName(name:str,db : Session = Depends(get_db)):
   return  UserController.getUsersByName(name,db)


@userRooter.post('/phone_token_sign_in')
async def checkPhoneAccessToken(token : str = Header(...)):
   return  TokenController.checkPhoneAccessToken(token)

@userRooter.patch('/admin/update/{id}')
async def adminUpdateUser(request :UpdateSchema,id,token : str = Header(...), db : Session = Depends(get_db)):
   print('aaaaaa')
   return  UserController.adminUpdateUser(id,db,request,token)

@userRooter.get('/admin')
async def isAdmin(token : str = Header(...),db : Session = Depends(get_db)):
   return  UserController.isAdmin(db,token=token)

@userRooter.post('/forget_password')
async def reset_password(email: str = Body(...), db: Session = Depends(get_db)):
   
    return UserController.resetPassword(email, db)

#check token validity
@userRooter.post('/phone_check_token')
async def check_token(db : Session = Depends(get_db),token : str = Header(...)):
   #print(f"{Header}")
   return  TokenController.checkPhoneAccessToken(token,db)

@userRooter.post('/sendEmails')
async def sendEmails(sendEmails:SendEmails):
   #print(f"{Header}")
   return  UserController.sendEmails(sendEmails)

@userRooter.get('/getAllUsers')
async def getAllUsers(page:int,limit:int,db : Session = Depends(get_db)):
   return  UserController.getAllUsers(limit,db,page)

@userRooter.get('/getuser/{email}')
async def getuser(email:str,db : Session = Depends(get_db)):
   return  UserController.getuser(email=email,db=db)

@userRooter.get('/getAll')
async def getAllUsers(db : Session = Depends(get_db)):
   return  UserController.getAll(db)

@userRooter.delete('/deleteUser/{id}')
async def delete_user(id:int,db : Session = Depends(get_db),token:str=Header(...)):
   return  UserController.deleteUser(token,id,db)

@userRooter.delete('/deleteUserPhone/{id}')
async def deletePhone(id:int,db : Session = Depends(get_db)):
   return  UserController.deletePhone(id,db)

@userRooter.delete('/deleteUserPhoneByPhoneNumber/{phone}')
async def deletePhone(phone:int,db : Session = Depends(get_db)):
   return  UserController.deletePhoneByPhneNumber(phone,db)
def get_table_names(db: Session = Depends(get_db)) -> List[str]:
    inspector = inspect(db)
    return inspector.get_table_names()

@userRooter.get('/dispalyadmin')
async def displayAdminDashboard(db:Session=Depends(get_db),token:str=Header(...)):
     return  UserController.displayAdminDashboard(db,token)



@userRooter.put("/users/{user_id}/change_password")
def change_password(user_id: int, change_password: UserChangePasswordSchema, db: Session = Depends(get_db)):
    return UserController.change_password(db, user_id=user_id, password=change_password.current_password, new_password=change_password.new_password)

@userRooter.put("/updateavatar/{user_id}")
async def updateavatar(user_id: int, picture: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    return await UserController.updateAvatar(user_id,picture,db)