from fastapi import APIRouter
from Schemas.ClaimSchema import ClaimSchema
import bcrypt
import jwt
import time
from fastapi import FastAPI,Depends,HTTPException,APIRouter,Header
from Controllers import ClaimController
from sqlalchemy.orm import Session
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Registration import Registration
from database.database import SessionLocal,get_db

claimRouter=APIRouter()

@claimRouter.post('/addClaim')
async def addClaim(des : str, db : Session = Depends(get_db)):
   
   return  ClaimController.add_Claim(des,db)

@claimRouter.put('/updateClaim/{idClaim}')
async def UpdateClaim(idClaim:int,des : str, db : Session = Depends(get_db)):
   
   return  ClaimController.update_Claim(idClaim,des,db)



@claimRouter.delete('/deleteClaim/{idClaim}')
async def UpdateClaim(idClaim:int, db : Session = Depends(get_db)):
   
   return  ClaimController.removeClaim(db,idClaim)