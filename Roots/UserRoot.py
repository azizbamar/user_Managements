
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

@userRooter.post('/userManagementService/user_sign_up')
async def signUp(request : Registration, db : Session = Depends(get_db)):
   return  UserController.signUp(request,db)

# Web Sign In
@userRooter.post('/userManagementService/user_sign_in')
async def signIn(request : Authentification, db : Session = Depends(get_db)):
   return  UserController.signIn(request,db)

@userRooter.post('/userManagementService/token_sign_in')
async def checkAccessToken(token : str = Header(...)):
   return  TokenController.checkAccessToken(token)


# Phone Sign In
@userRooter.post('/userManagementService/user_sign_in_from_phone')
async def signInFromPhone(request : PhoneAuthentification, db : Session = Depends(get_db)):
   return  UserController.signInFromPhone(request,db)

# Web Sign Out
@userRooter.post('/userManagementService/user_sign_out')
async def signOut(db : Session = Depends(get_db),token : str = Header(...)):
   return  UserController.signOut(db,token)

# Phone Sign Out
@userRooter.post('/userManagementService/user_sign_out_from_phone')
async def signOutFromPhone(db : Session = Depends(get_db),token : str = Header(...)):
   return  UserController.signOutFromPhone(db,token)

#update account
@userRooter.post('/userManagementService/update_account')
async def updateUser(request : Registration,db : Session = Depends(get_db),token : str = Header(...)):
   return  UserController.updateUser(request,token,db)

#delete Phone
@userRooter.post('/userManagementService/removePhone/{user_id}')
async def deletePhone(user_id:int,db : Session = Depends(get_db)):
   return  UserController.removePhoneForUser(user_id,db)

# chercher users

@userRooter.get('/userManagementService/users/{name}')
async def getUsersByName(name:str,db : Session = Depends(get_db)):
   return  UserController.getUsersByName(name,db)


@userRooter.post('/userManagementService/phone_token_sign_in')
async def checkPhoneAccessToken(token : str = Header(...)):
   return  TokenController.checkPhoneAccessToken(token)

@userRooter.patch('/userManagementService/admin/update/{id}')
async def adminUpdateUser(request :UpdateSchema,id,token : str = Header(...), db : Session = Depends(get_db)):
   print('aaaaaa')
   return  UserController.adminUpdateUser(id,db,request,token)

@userRooter.get('/userManagementService/admin')
async def isAdmin(token : str = Header(...),db : Session = Depends(get_db)):
   return  UserController.isAdmin(db,token=token)

@userRooter.post('/userManagementService/forget_password')
async def reset_password(email: str = Body(...), db: Session = Depends(get_db)):
   
    return UserController.resetPassword(email, db)

#check token validity
@userRooter.post('/userManagementService/phone_check_token')
async def check_token(db : Session = Depends(get_db),token : str = Header(...)):
   #print(f"{Header}")
   return  TokenController.checkPhoneAccessToken(token,db)

@userRooter.post('/userManagementService/sendEmails')
async def sendEmails(sendEmails:SendEmails):
   #print(f"{Header}")
   return  UserController.sendEmails(sendEmails)

@userRooter.get('/userManagementService/getAllUsers')
async def getAllUsers(page:int,limit:int,db : Session = Depends(get_db)):
   return  UserController.getAllUsers(limit,db,page)

@userRooter.get('/userManagementService/getuser/{email}')
async def getuser(email:str,db : Session = Depends(get_db)):
   return  UserController.getuser(email=email,db=db)

@userRooter.get('/userManagementService/getAll')
async def getAllUsers(db : Session = Depends(get_db)):
   return  UserController.getAll(db)

@userRooter.delete('/userManagementService/deleteUser/{id}')
async def delete_user(id:int,db : Session = Depends(get_db),token:str=Header(...)):
   return  UserController.deleteUser(token,id,db)

@userRooter.delete('/userManagementService/deleteUserPhone/{id}')
async def deletePhone(id:int,db : Session = Depends(get_db)):
   return  UserController.deletePhone(id,db)

@userRooter.delete('/userManagementService/deleteUserPhoneByPhoneNumber/{phone}')
async def deletePhone(phone:int,db : Session = Depends(get_db)):
   return  UserController.deletePhoneByPhneNumber(phone,db)
def get_table_names(db: Session = Depends(get_db)) -> List[str]:
    inspector = inspect(db)
    return inspector.get_table_names()

@userRooter.get('/userManagementService/dispalyadmin')
async def displayAdminDashboard(db:Session=Depends(get_db),token:str=Header(...)):
     return  UserController.displayAdminDashboard(db,token)



@userRooter.put("/userManagementService/users/{user_id}/change_password")
def change_password(user_id: int, change_password: UserChangePasswordSchema, db: Session = Depends(get_db)):
    return UserController.change_password(db, user_id=user_id, password=change_password.current_password, new_password=change_password.new_password)

@userRooter.put("/userManagementService/updateavatar/{user_id}")
async def updateavatar(user_id: int, picture: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    return await UserController.updateAvatar(user_id,picture,db)