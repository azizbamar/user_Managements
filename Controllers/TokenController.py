from Schemas import Hasher
import time
from fastapi import FastAPI, HTTPException, Depends,Header,status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
# import jwt
from jose import jwt,JWTError
from sqlalchemy import exc
from database.database import SessionLocal,get_db
from settings import ALGORITHMS, SECRET,ALGORITHM
from models.Phone import Phone
from models.PhoneHistory import PhoneHistory
from models.Token import Token
from models.User import User
from contextlib import contextmanager
from errors import *
def createAccessToken(user,password,db):
    payload =createPayload(user,24)
    if Hasher.verify_password(password, user.password):
       
        access_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
        token = Token(token = access_token ,user = user)
        addToken(token,db)
        u=checkAccessToken(access_token)["user"]
        return {"user":u,"access_token": access_token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="wrong email or password")



# def createAccessTokenWithoutPhone(user,password,db):
#     import pdb; pdb.set_trace()
#     payload =createPayload(user,60)
#     if Hasher.verify_password(password, user.password):
#         access_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
#         userHasPhone = db.query(Phone).filter(Phone.user_id == user.id).first()
#         if (not (userHasPhone)) and (userHasPhone.uid):
#             phone = Phone(phoneToken = access_token , user = user , rememberMe = False)
#             db.add(phone)
#             db.commit()
#             return access_token   
#         else:
#             userHasPhone.phoneToken = access_token
#             db.commit()

#             return access_token   
#     else:
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED ,detail="wrong email or password")

# CREATE ACCESS TOKEN FOR PHONE
def createAccessTokenPhone(user,password,phone,rememberMe,db):
    import pdb; pdb.set_trace()
    
    if Hasher.verify_password(password, user.password):
        
        phoneExist = db.query(Phone).filter(Phone.uid == phone.uid).first()
        if (phoneExist):
            if (phoneExist.rememberMe):
                #60 days=60*24 hour
                nbhours=24*60
                payload =createPayload(user,nbhours)
                access_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
                samePhone = db.query(Phone).filter(Phone.user_id == user.id).first()
                if (samePhone):
                    samePhone.rememberMe = rememberMe
                    samePhone.phoneToken = access_token
                    db.commit()
                    return access_token
                else:
                    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail=("UNAUTHORIZED"))
            else:
                # token :one day: 24 hour
                payload =createPayload(user,24)
                access_token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
                phoneExist.user = user
                phoneExist.rememberMe = rememberMe
                phoneExist.phoneToken = access_token
                db.commit()
                return access_token
        else:
            if (createPhoneIfNotExist(phone,access_token,user,rememberMe,db)):
                return access_token
            else:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail="Forbidden")
               
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="wrong email or password")


                

            



def checkPhoneAccessToken(phoneToken,db):
    print(phoneToken)
    try:
        if(phoneToken):
            decoded_token = jwt.decode(phoneToken, SECRET,algorithms=ALGORITHMS)
            print(decoded_token)
            if (decoded_token):
                
                if (time.time() < decoded_token['exp']):
                    tokenExist =  db.query(Phone).filter(Phone.phoneToken == phoneToken).first()
                    if (tokenExist):
                        print(tokenExist)
                        return True
                    else:
                        raise HTTPException(status_code=404,detail="token not found")
                else:
                    raise HTTPException(status_code=400 , detail= "session expired")
        else:
            raise HTTPException(status_code=404,detail="token not found")
    except JWTError:
        raise HTTPException(status_code=500 , detail= "Invalid token")
    
# CHECK ACCESS TOKEN VALIDITY
def checkAccessToken(token):
    with contextmanager(get_db)() as db :
        try:
            decoded_token = jwt.decode(token, SECRET,algorithms=ALGORITHMS)
            print('aaa')
            if (time.time() <= decoded_token['exp']):
                print('aaa')
                tokenExist = db.query(Token).filter(Token.token == token).first()
                print('aaa')
                if (tokenExist):
                    print(time.time())
                    print(decoded_token['exp']) 
                    email=decoded_token["email"]
                    return dict({"user":get_user(email,db)})
                else:              
                    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="unauthorized")
            else:
                print('session expired')
                raise HTTPException(status_code=HTTP_403_FORBIDDEN , detail= "session expired")
        except JWTError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED,detail="invalid token")

# ADD TOKEN 
def addToken(token,db):
    try:
        db.add(token)
        db.commit()
        return dict({"detail":"Token addded"})
            
    except exc.IntegrityError as e:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN,detail="Phone already connected")
    
# CREATE PHONE IF NOT EXIST
def createPhoneIfNotExist(phone,phoneToken,user,rememberMe,db):
    try: 
        UserPhoneExist = db.query(Phone).filter(Phone.user_id == user.id).first()
        if not (UserPhoneExist):
            phone = Phone(uid = phone.uid,user = user,model=phone.model,osVersion = phone.osVersion, phoneToken = phoneToken ,rememberMe = rememberMe)
            try :
                phoneHistory = PhoneHistory(uid = phone.uid,model=phone.model,osVersion = phone.osVersion, phoneToken = phone.phoneToken)
                db.add(phoneHistory)
                db.add(phone)
                db.commit()
                return True
            except Exception :
                raise  HTTPException (status_code=HTTP_401_UNAUTHORIZED,detail="Phone already exist") 
        else:
            return False 
    except Exception :
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error Has been Occured")  

# CREATE TOKEN'S PAYLOAD 
def createPayload(user,nbHour):
    return {
            "email" : user.email,
            "exp" : time.time()+(nbHour*60*60)
        }
# GET USER DATA
def get_user(email: str,db):
  try: 
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user
  except Exception :
        raise  HTTPException (status_code=HTTP_500_INTERNAL_SERVER_ERROR,detail="Error has been Occured")  