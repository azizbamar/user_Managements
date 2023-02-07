from Schemas import Hasher
import time
from fastapi import FastAPI, HTTPException, Depends,Header,status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
# import jwt
from jose import jwt,JWTError
from sqlalchemy import exc
from database.database import SessionLocal,get_db
from models.Phone import Phone
from models.PhoneHistory import PhoneHistory
from models.Token import Token
from models.User import User
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
    
def createAccessTokenWithoutPhone(user,password,db):
    payload =createPayload(user,60)
    if Hasher.verify_password(password, user.password):
        access_token = jwt.encode(payload, "secret", algorithm="HS256")
        userHasPhone = db.query(Phone).filter(Phone.user_id == user.id).first()
        if not (userHasPhone) or (userHasPhone.uid!= None):
            phone = Phone(phoneToken = access_token , user = user)
            db.add(phone)
            db.commit()
            return access_token
        else:
            raise HTTPException(status_code= 400 , detail="unhautirized")

# CREATE ACCESS TOKEN FOR PHONE
def createAccessTokenPhone(user,password,phone,db):
    payload =createPayload(user,60)
    if Hasher.verify_password(password, user.password):
        access_token = jwt.encode(payload, "secret", algorithm="HS256")        
        if  not (createPhoneIfNotExist(phone=phone,phoneToken = access_token ,user=user,db=db)):
            samePhone = db.query(Phone).filter(Phone.uid == phone.uid).first()
            if (samePhone):
                tokenvalid= checkPhoneAccessToken(samePhone.phoneToken,samePhone.uid,db)
                if not (tokenvalid):
                    samePhone.phoneToken = access_token
                    phoneHistory = PhoneHistory(uid = samePhone.uid,modele=samePhone.modele,osVersion = samePhone.osVersion, phoneToken = samePhone.phoneToken)
                    db.add(phoneHistory)
                    db.commit()
                else:
                    raise HTTPException(status_code=400,detail="unhaoutorized")
            else:
                raise HTTPException(status_code=400,detail="unhaoutorized")
        return {"access_token": access_token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=400, detail="wrong email or password")

def checkPhoneAccessToken(phoneToken,uid,db):
    try:
        if(phoneToken):
            decoded_token = jwt.decode(phoneToken, "secret",algorithms=['HS256'])
            if (decoded_token):
                if (time.time() < decoded_token['exp']):
                    phone = db.query(Phone).filter(Phone.uid == uid).first()
                    tokenExist = phone.phoneToken
                    if (tokenExist):
                        return True
                    else:
                        return False
            else:
                raise HTTPException(status_code=400 , detail= "session expired")
    except JWTError:
        raise HTTPException(status_code=500 , detail= "Error as been occured")
    
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

# ADD TOKEN 
def addToken(token,db):
    try:
        db.add(token)
        db.commit()
        return dict({"detail":"Token addded"})
            
    except exc.IntegrityError as e:
        raise HTTPException(status_code=400,detail="Phone already connected")
    
# CREATE PHONE IF NOT EXIST
def createPhoneIfNotExist(phone,phoneToken,user,db):
    try: 
        UserPhoneExist = db.query(Phone).filter(Phone.user_id == user.id).first()
        if not (UserPhoneExist):
            phone = Phone(uid = phone.uid,user = user,modele=phone.modele,osVersion = phone.osVersion, phoneToken = phoneToken )
            try :
                phoneHistory = PhoneHistory(uid = phone.uid,modele=phone.modele,osVersion = phone.osVersion, phoneToken = phone.phoneToken)
                db.add(phoneHistory)
                db.add(phone)
                db.commit()
                return True
            except Exception :
                raise  HTTPException (status_code=409,detail="Phone already exist") 
        else:
            return False
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