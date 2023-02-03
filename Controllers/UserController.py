from Controllers.TokenController import createAccessToken,createAccessTokenPhone, invalidateToken
from Schemas.Authentification import Authentification
from Schemas.PhoneAuthentification import PhoneAuthentification
from Schemas.Hasher import hash_password
from Schemas.Registration import Registration
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.User import User,user_roles
from sqlalchemy import exc
from fastapi import FastAPI,Depends,HTTPException,Header
from Schemas.UserSchema import UserSchema
from models.Role import Role
def getRoleByName(db,name):
    return db.query(Role).filter(Role.name == name).first()

# sign Up

def signUp(request : Registration ,db):
    hashed_password = hash_password(request.password)
    listRolesNames=request.roles
    listRoles=list()
    for role in listRolesNames  :
        listRoles.append(getRoleByName(db,role))

    user = User(email = request.email , password = hashed_password, name = request.name ,telephoneNumber = request.telephoneNumber,roles=listRoles)
    try:
        db.add(user)
        db.commit() 
        return {"detail":"register succedded"}
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400,detail="this email is used")

#login for guests and web application

def signIn(request : Authentification , db):
    user = db.query(User).filter(User.email == request.email).first()
    if (user):
        token=createAccessToken(user,request.password,db)
        return  token
    else:
        raise HTTPException(status_code=400,detail="wrong email or password")


#login for phones

def PhonesignIn(request :PhoneAuthentification  , db):
    user = db.query(User).filter(User.email == request.email).first()
    if  (user):
            if not (request.rememberME):
                token=createAccessToken(user,request.password,db)
                return  token
            else:
                token=createAccessTokenPhone(user,request.password,request.phone,db)
                return token
    else:
            raise HTTPException(status_code=400,detail="wrong email or password")



#logout

def signOut(db,token):
    return invalidateToken(db,token)


 
