import inspect
from typing import List
from fastapi import APIRouter
from Schemas.RoleSchema import RoleSchema
import bcrypt
import jwt
import time
from fastapi import FastAPI,Depends,HTTPException,APIRouter,Header

from Controllers import RoleController
from sqlalchemy.orm import Session
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Registration import Registration
from database.database import SessionLocal,get_db,get_table_names

userRooter = APIRouter()


roleRouter=APIRouter()

@roleRouter.post('/addRole')
async def addRole(role : RoleSchema, db : Session = Depends(get_db)):
   
   return  RoleController.add_role(role,db)

@roleRouter.put('/updateRole/{idRole}')
async def UpdateRole(idRole:int,role : RoleSchema, db : Session = Depends(get_db)):
   
   return  RoleController.update_role(role,idRole,db)



@roleRouter.put('/deleteRole/{idRole}')
async def deleteRole(idRole:int, db : Session = Depends(get_db)):
   
   return  RoleController.delete_role(idRole,db)
   
@roleRouter.get('/userRole/{id}')
async def getUserRoles(id:int,db : Session = Depends(get_db)):   
   return  RoleController.getUserRolesById(user_id=id,db=db)

@roleRouter.get('/claims/')
async def getAllClaims(db : Session = Depends(get_db)):
   return  RoleController.getAllClaims(db)

@roleRouter.get('/roles')
async def getAllRoles(db : Session = Depends(get_db)):
   
   return  RoleController.getAllRoles(db)


@roleRouter.get('/role/getAllRolesNames')
async def getRoles(db : Session = Depends(get_db)):
   
   return  RoleController.getAllRoleNames(db)
@roleRouter.delete('/deleteRole/{id}')
async def deleteRole(id:int,db : Session = Depends(get_db)):
   
   return  RoleController.delete_role(id,db)


@roleRouter.get('/table', response_model=List[str])
async def getRoles(db: Session = Depends(get_db)):
   #  inspector = inspect(db)
    table_names =get_table_names(db)
    return table_names


@roleRouter.get('/alltags/')
async def getRoles(db: Session = Depends(get_db)):
    all_merged_tags = RoleController.get_all_merged_tags(db)
   #  inspector = inspect(db)
    
    return all_merged_tags