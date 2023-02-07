
from fastapi import Depends,APIRouter,Header
from Controllers import UserController
from sqlalchemy.orm import Session
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Registration import Registration
from database.database import get_db
userRooter = APIRouter()

@userRooter.post('/user_sign_up')
async def signUp(request : Registration, db : Session = Depends(get_db)):
   return  UserController.signUp(request,db)

# Web Sign In
@userRooter.post('/user_sign_in')
async def signIn(request : Authentification, db : Session = Depends(get_db)):
   return  UserController.signIn(request,db)
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