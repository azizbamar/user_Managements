from fastapi import APIRouter
from Schemas.RoleSchema import RoleSchema
import bcrypt
import jwt
import time
from fastapi import FastAPI,Depends,HTTPException,APIRouter,Header
from models.User import user_roles
from Controllers import RoleController
from sqlalchemy.orm import Session
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Registration import Registration
from database.database import SessionLocal,get_db

userRooter = APIRouter()


roleRouter=APIRouter()

@roleRouter.post('/addRole')
async def addRole(role : RoleSchema, db : Session = Depends(get_db)):
   
   return  RoleController.add_role(role,db)

@roleRouter.put('/updateRole/{idRole}')
async def UpdateRole(idRole:int,role : RoleSchema, db : Session = Depends(get_db)):
   
   return  RoleController.update_role(role,idRole,db)



@roleRouter.put('/deleteRole/{idRole}')
async def UpdateRole(idRole:int, db : Session = Depends(get_db)):
   
   return  RoleController.delete_role(idRole,db)
   

@roleRouter.get('/role/getAllRolesNames')
async def getRoles(db : Session = Depends(get_db)):
   
   return  RoleController.getAllRoleNames(db)