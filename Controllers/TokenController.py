from Schemas import Hasher
import bcrypt,time
from fastapi import FastAPI, HTTPException, Depends,Header,status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
# import jwt
import asyncio
from jose import jwt,JWTError
from sqlalchemy import exc
from database.database import SessionLocal,get_db
from models.Phone import Phone
from models.Token import PhoneToken, Token
from models.User import User
from models.Role import Role
from sqlalchemy.orm import Session
from contextlib import contextmanager


def createAccessToken(user,password,db):
    
    payload =createPayload(user,1)
    if Hasher.verify_password(password, user.password):
       
        access_token = jwt.encode(payload, "secret", algorithm="HS256")
        token = Token(token = access_token ,user = user)
        addToken(token,db)

        return {"user":checkAccessToken(access_token),"access_token": access_token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=400, detail="wrong email or password")


# CREATE ACCESS TOKEN FOR PHONE
def createAccessTokenPhone(user,password,phone,db):
    payload =createPayload(user,60)
    if Hasher.verify_password(password, user.password):
        access_token = jwt.encode(payload, "secret", algorithm="HS256")
        phoneToken = PhoneToken(token = access_token ,user = user,phone_id = phone.uid)
        
        createPhoneIfNotExist(phone=phone,user=user,db=db)
        samePhone = db.query(Phone).filter(Phone.uid == phone.uid).first()
        if not(samePhone):
          raise HTTPException(status_code=400,detail="phone already connected")

        
        addToken(phoneToken,db)
        
        return {"user":checkAccessToken(access_token),"access_token": access_token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=400, detail="wrong email or password")


# ADD TOKEN 
def addToken(token,db):
    try:
            db.add(token)
            db.commit()
            return dict({"detail":"Token addded"})
            
    except exc.IntegrityError as e:
            raise HTTPException(status_code=400,detail="Phone already connected")

# CHECK ACCESS TOKEN VALIDITY
def checkAccessToken(token : str = Header(...)):
    with contextmanager(get_db)() as db :
        try:
            decoded_token = jwt.decode(token, "secret",algorithms=['HS256'])
            if (time.time() < decoded_token['exp']):
                tokenExist = db.query(Token).filter(Token.token == token).first()
                if (tokenExist):
                    email=decoded_token["email"]
                    return get_user(email,db)
                else:
                    raise HTTPException(status_code=400,detail="unauthorized")
            else:
                raise HTTPException(status_code=400 , detail= "session expired")
        except JWTError:
            raise HTTPException(status_code=400,detail="invalid token")


# INVALIDATE TOKEN
def invalidateToken(db,token):
    try:
        decoded_token = jwt.decode(token, "secret",algorithms=['HS256'])
       
        decoded_token["exp"]=0
        
        if (decoded_token):
            
            phonetoken=db.query(PhoneToken).filter(PhoneToken.token == token).delete()

            if not phonetoken:
        
              db.query(Token).filter(Token.token == token).delete()
            
        db.commit()
        return dict({"detail":"Logout succedded"})
    except JWTError:
        raise HTTPException(status_code=400,detail="invalid token")

# CREATE PHONE IF NOT EXIST
def createPhoneIfNotExist(phone,user,db):
   try: 
    UserPhoneExist = db.query(Phone).filter(Phone.user_id == user.id).first()

    if not (UserPhoneExist):
        
    
        phone = Phone(uid = phone.uid,user = user,modele=phone.modele,androidVersion=phone.androidVersion)
        try :
            db.add(phone)
            
            db.commit()
        except Exception :

            raise  HTTPException (status_code=409,detail="Phone already exist") 


   except Exception :

        raise  HTTPException (status_code=500,detail="Error Has been Occured")      


    


# CREATE TOKEN'S PAYLOAD 
def createPayload(user,nbHour):
    return {
            "email" : user.email,
            "exp" : time.time()+nbHour*3600*24
        }

# GET USER DATA
def get_user(email: str,db):
  try: 
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
  except Exception :

        raise  HTTPException (status_code=500,detail="Error has been Occured")  