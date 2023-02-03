from Schemas import Hasher
import bcrypt,time
from fastapi import FastAPI, HTTPException, Depends,Header,status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
# import jwt
import asyncio
from jose import JWTError,jwt
from sqlalchemy import exc
from models.Phone import Phone
from models.Token import Token
from models.User import User,user_roles
from models.Role import Role


def get_user(email: str,db ):
   
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    print('get user function')
    return user


def createAccessToken(user,password,db):
    
    payload =createPayload(user)
    if Hasher.verify_password(password, user.password):
       
        access_token = jwt.encode(payload, "secret", algorithm="HS256")
        
        token = Token(token = access_token ,user = user)
        addToken(token,db)

        return {"user":checkAccessToken(db,access_token),"access_token": access_token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=400, detail="wrong email or password")

def createAccessTokenPhone(user,password,phone,db):
    
    payload =createPayload(user)
    if Hasher.verify_password(password, user.password):
        access_token = jwt.encode(payload, "secret", algorithm="HS256")
        token = Token(token = access_token ,user = user)
        addToken(token,db)
        createPhoneIfNotExist(phone=phone,user=user,db=db)
        return {"user":checkAccessToken(db,access_token),"access_token": access_token, "token_type": "Bearer"}
    else:
        raise HTTPException(status_code=400, detail="wrong email or password")

# def getUserRoles(token,db):
#     user=checkAccessToken(db,token)
#     userId=user.id
#     userRoles=db.query(user_roles).filter(user_roles.user_id== userId).all()
#     print(userRoles)
#     return (userRoles)



def addToken(token,db):
    try:
            db.add(token)
            db.commit()
            db.refresh(token)
    except exc.IntegrityError as e:
            raise HTTPException(status_code=400,detail="error has been occured")


def checkAccessToken(db,token : str = Header(...)):
    

    try:
        decoded_token = jwt.decode(token, "secret",algorithms=['HS256'])
        print(decoded_token)
        tokenExist = db.query(Token).filter(Token.token == token).first()
        print(tokenExist)
        if (tokenExist):
            email=decoded_token["email"]
            return get_user(email,db)
        else:
            raise HTTPException(status_code=400,detail="unauthorized")

    except JWTError:
        raise HTTPException(status_code=400,detail="invalid token")





def invalidateToken(db,token):
    try:
        decoded_token = jwt.decode(token, "secret",algorithms=['HS256'])
        if (decoded_token):
            print(token)
            db.query(Token).filter(Token.token == token).delete()
            db.commit()
    except JWTError:
        raise HTTPException(status_code=400,detail="invalid token")


def createPhoneIfNotExist(phone,user,db):
    UserPhoneExist = db.query(Phone).filter(Phone.user_id == user.id).first()
    if not (UserPhoneExist):
        phone = Phone(uid = phone.uid,user = user,modele=phone.modele,androidVersion=phone.androidVersion)
        db.add(phone)
        db.commit()
    else:
        raise HTTPException(status_code=400,detail="User already connected By Other Phone")

def createPayload(user):
    return {
            "email" : user.email,
            "expires" : time.time()+600
        }