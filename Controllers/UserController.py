from Controllers.TokenController import createAccessToken, invalidateToken
from Schemas.Authentification import Authentification
from Schemas.Hasher import hash_password
from Schemas.Registration import Registration
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.User import User,user_roles
from sqlalchemy import exc
from fastapi import FastAPI,Depends,HTTPException,Header
from Schemas.UserSchema import UserSchema
from models.Role import Role
def getRoleById(db,idrole):
    return db.query(Role).filter(Role.id == idrole).first()

def signUp(request : Registration ,db):
    hashed_password = hash_password(request.password)
    listRegistrationId=request.roles
    listRoles=list()
    for x in listRegistrationId  :
        listRoles.append(getRoleById(db,int(x)))

    user = User(email = request.email , password = hashed_password, name = request.name ,telephoneNumber = request.telephoneNumber,roles=listRoles)
    try:
        db.add(user)
        db.commit()
       
        
        
        return {"detail":"register succedded"}
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400,detail="this email is used")


def signIn(request : Authentification , db):
    user = db.query(User).filter(User.email == request.email).first()
    if (user):
        token=createAccessToken(user,request.password,request.clientType,request.phoneId,db)
        return  token
    else:
        raise HTTPException(status_code=400,detail="wrong email or password")


def signOut(db,token):
    return invalidateToken(db,token)


 
