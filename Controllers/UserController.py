from Controllers.TokenController import createAccessToken
from Schemas.Authentification import Authentification
from Schemas.Hasher import hash_password
from Schemas.Registration import Registration
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.User import User
from sqlalchemy import exc
from fastapi import FastAPI,Depends,HTTPException


def signUp(request : Registration ,db):
    hashed_password = hash_password(request.password)
    user = User(email = request.email , password = hashed_password, username = request.username ,telephoneNumber = request.telephoneNumber)
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400,detail="this email is used")


def signIn(request : Authentification , db):
    user = db.query(User).filter(User.email == request.email).first()
    if (user):
        return createAccessToken(user,request.password,db)
    else:
        raise HTTPException(status_code=400,detail="wrong email or password")


 
